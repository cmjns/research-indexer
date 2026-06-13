"""
ri — research-indexer CLI

Thin wrapper over the service layer. No business logic here.

Usage:
    ri corpus scan <path> [--glob "**/*.txt"] [--level work] [--out corpus.json]
    ri germ detect <corpus.json> [--min-displacement 0.01]
    ri germ supply <corpus.json> --label "..." --cycle <id> [<id> ...]
    ri passage <corpus.json> --germ <germ.json> [--steps N] [--out eddy.json]
    ri eddy show <eddy.json>
    ri session list
"""

import argparse
import json
import sys
from pathlib import Path


def cmd_corpus_scan(args):
    from corpus.directory import DirectoryProvider
    from extract.nlp import NLPExtractor
    from core.field import PotentialField

    provider = DirectoryProvider(
        path=args.path,
        glob=args.glob,
        medium_format=args.medium,
    )
    extractor = NLPExtractor()

    records = []
    for domain in provider.domains(level=args.level):
        net = extractor.extract(domain)
        records.append({
            "domain_id":     domain.id,
            "domain_level":  domain.definition.name,
            "source_file":   domain.metadata.get("source_file", ""),
            "simplex_count": len(net),
            "term_count":    len(net.terms()),
            "simplexes": [
                {
                    "id":        s.id,
                    "source":    s.source.label,
                    "target":    s.target.label,
                    "modulator": s.modulator.label,
                    "intensity": s.intensity,
                    "asymmetry": s.asymmetry,
                    "gain":      s.gain,
                }
                for s in net.simplexes.values()
            ],
        })

    out = {
        "provider": provider.name,
        "level":    args.level,
        "domains":  records,
    }
    outfile = args.out or "corpus.json"
    Path(outfile).write_text(json.dumps(out, indent=2))
    total_s = sum(r["simplex_count"] for r in records)
    print(f"Scanned {len(records)} domain(s), {total_s} simplexes → {outfile}")


def cmd_germ_detect(args):
    from services.germ_service import GermService
    corpus = _load_corpus(args.corpus_file)
    network = _corpus_to_network(corpus)
    service = GermService(min_displacement=args.min_displacement)
    germs = service.detect(network)

    print(f"Found {len(germs)} candidate germ(s):\n")
    for i, g in enumerate(germs):
        print(f"  [{i}] {g.label}")
        print(f"       displacement={g.pattern.displacement:.4f}  "
              f"modulator_stable={g.pattern.modulator_stable}")
        print(f"       cycle={g.pattern.cycle}\n")


def cmd_germ_supply(args):
    corpus = _load_corpus(args.corpus_file)
    network = _corpus_to_network(corpus)
    from services.germ_service import GermService
    service = GermService()
    germ = service.supply(
        label=args.label,
        simplex_ids=args.cycle,
        network=network,
        notes=args.notes or "",
    )
    out = {
        "id":               germ.id,
        "label":            germ.label,
        "source":           germ.source.value,
        "cycle":            germ.pattern.cycle,
        "modulator_stable": germ.pattern.modulator_stable,
        "displacement":     germ.pattern.displacement,
        "notes":            germ.notes,
    }
    outfile = args.out or "germ.json"
    Path(outfile).write_text(json.dumps(out, indent=2))
    print(f"Germ saved → {outfile}  (displacement={germ.pattern.displacement:.4f})")


def cmd_passage(args):
    from services.passage_service import PassageService
    from extract.nlp import NLPExtractor
    from corpus.directory import DirectoryProvider
    from core.germ import Germ, GermSource, RoleRotation
    import uuid

    corpus = _load_corpus(args.corpus_file)

    with open(args.germ) as f:
        germ_data = json.load(f)
    pattern = RoleRotation(
        cycle=germ_data["cycle"],
        modulator_stable=germ_data.get("modulator_stable", True),
        displacement=germ_data.get("displacement", 0.0),
    )
    germ = Germ(
        id=germ_data.get("id", str(uuid.uuid4())),
        label=germ_data.get("label", "unnamed"),
        source=GermSource(germ_data.get("source", "analyst")),
        pattern=pattern,
    )

    provider = DirectoryProvider(
        path=corpus["_source_path"],
        glob=corpus.get("_glob", "**/*.txt"),
    )
    service = PassageService(extractor=NLPExtractor())
    sid = service.new_session(provider, germ)
    eddy = service.run(sid, max_steps=args.steps, halt_on_stable=True)

    print(f"\nPassage complete — {len(eddy.steps)} steps")
    print(f"Interference: {eddy.interference_character.value if eddy.interference_character else '—'}")
    print(f"Operative zero: {eddy.operative_zero}")
    print(f"Role rotations: {len(eddy.vocabulary_rotations)}")
    print(f"Remainder entries: {len(eddy.remainder)}")
    print(f"\nWhat appeared:\n  {eddy.what_appeared}")

    outfile = args.out or "eddy.json"
    Path(outfile).write_text(json.dumps(eddy.to_ledger_entry(), indent=2))
    print(f"\nEddy saved → {outfile}")


def cmd_eddy_show(args):
    with open(args.eddy_file) as f:
        data = json.load(f)
    print(json.dumps(data, indent=2))


# ------------------------------------------------------------------
# Shared helpers
# ------------------------------------------------------------------

def _load_corpus(path: str) -> dict:
    with open(path) as f:
        return json.load(f)

def _corpus_to_network(corpus: dict):
    from core.network import SimplexNetwork
    from core.simplex import Simplex
    from core.term import Term
    network = SimplexNetwork()
    for domain in corpus.get("domains", []):
        for s in domain.get("simplexes", []):
            simplex = Simplex(
                id=s["id"],
                source=Term(id=s["source"], label=s["source"]),
                target=Term(id=s["target"], label=s["target"]),
                modulator=Term(id=s["modulator"], label=s["modulator"]),
                intensity=s["intensity"],
                asymmetry=s["asymmetry"],
                gain=s["gain"],
            )
            network.add(simplex)
    return network


# ------------------------------------------------------------------
# CLI wiring
# ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="ri",
        description="research-indexer — a passage engine for texts",
    )
    sub = parser.add_subparsers(dest="command")

    # corpus
    p_corpus = sub.add_parser("corpus", help="Corpus operations")
    corpus_sub = p_corpus.add_subparsers(dest="corpus_command")
    p_scan = corpus_sub.add_parser("scan", help="Scan a directory into a corpus file")
    p_scan.add_argument("path")
    p_scan.add_argument("--glob",   default="**/*.txt")
    p_scan.add_argument("--level",  default="work")
    p_scan.add_argument("--medium", default="plaintext")
    p_scan.add_argument("--out",    default=None)

    # germ
    p_germ = sub.add_parser("germ", help="Detect or supply a germ")
    germ_sub = p_germ.add_subparsers(dest="germ_command")

    p_detect = germ_sub.add_parser("detect")
    p_detect.add_argument("corpus_file")
    p_detect.add_argument("--min-displacement", type=float, default=0.01)

    p_supply = germ_sub.add_parser("supply")
    p_supply.add_argument("corpus_file")
    p_supply.add_argument("--label",  required=True)
    p_supply.add_argument("--cycle",  nargs="+", required=True)
    p_supply.add_argument("--notes",  default="")
    p_supply.add_argument("--out",    default="germ.json")

    # passage
    p_pass = sub.add_parser("passage", help="Run a passage through a corpus")
    p_pass.add_argument("corpus_file")
    p_pass.add_argument("--germ",  required=True)
    p_pass.add_argument("--steps", type=int, default=50)
    p_pass.add_argument("--out",   default=None)

    # eddy
    p_eddy = sub.add_parser("eddy", help="Inspect an eddy")
    eddy_sub = p_eddy.add_subparsers(dest="eddy_command")
    p_show = eddy_sub.add_parser("show")
    p_show.add_argument("eddy_file")

    args = parser.parse_args()

    if args.command == "corpus" and args.corpus_command == "scan":
        cmd_corpus_scan(args)
    elif args.command == "germ":
        if args.germ_command == "detect":
            cmd_germ_detect(args)
        elif args.germ_command == "supply":
            cmd_germ_supply(args)
        else:
            p_germ.print_help()
    elif args.command == "passage":
        cmd_passage(args)
    elif args.command == "eddy" and args.eddy_command == "show":
        cmd_eddy_show(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
