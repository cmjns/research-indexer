"""
ri — research-indexer CLI

Thin wrapper over the service layer. No business logic here.

Usage:
    ri ingest <source> [--domain sentence] [--medium plaintext]
    ri germ detect <network_file>
    ri germ supply <network_file> --label "..." --cycle <id> [<id> ...]
    ri crystallize <network_file> --germ <germ_file> [--steps N]
    ri analyze <session_file> [--map] [--phases] [--report json|text]
    ri session list

Run `ri --help` or `ri <command> --help` for details.
"""

import argparse
import json
import sys


def cmd_ingest(args):
    from core.domain import DomainRegistry, Medium, Domain
    from extract.nlp import NLPExtractor
    import uuid

    registry = DomainRegistry()
    defn = registry.get(args.domain)
    medium = Medium(format=args.medium)

    with open(args.source, "r", encoding="utf-8") as f:
        content = f.read()

    domain = Domain(
        id=str(uuid.uuid4()),
        definition=defn,
        content=content,
        medium=medium,
    )

    extractor = NLPExtractor()
    network = extractor.extract(domain)

    out = {
        "domain_id": domain.id,
        "domain_level": defn.name,
        "simplex_count": len(network),
        "term_count": len(network.terms()),
        "simplexes": [
            {
                "id": s.id,
                "source": s.source.label,
                "target": s.target.label,
                "modulator": s.modulator.label,
                "intensity": s.intensity,
                "asymmetry": s.asymmetry,
                "gain": s.gain,
            }
            for s in network.simplexes.values()
        ],
    }

    outfile = args.out or "network.json"
    with open(outfile, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Extracted {len(network)} simplexes over {len(network.terms())} terms → {outfile}")


def cmd_germ_detect(args):
    from services.germ_service import GermService
    from core.network import SimplexNetwork
    from core.simplex import Simplex
    from core.term import Term

    network = _load_network(args.network_file)
    service = GermService(min_displacement=args.min_displacement)
    germs = service.detect(network)

    print(f"Found {len(germs)} candidate germ(s):\n")
    for i, g in enumerate(germs):
        print(f"  [{i}] {g.label}")
        print(f"       displacement={g.pattern.displacement:.4f}  "
              f"modulator_stable={g.pattern.modulator_stable}")
        print(f"       cycle={g.pattern.cycle}")
        print()


def cmd_crystallize(args):
    from services.crystallize_service import CrystallizeService
    from services.germ_service import GermService
    from core.germ import Germ, GermSource, RoleRotation
    import uuid

    network = _load_network(args.network_file)

    with open(args.germ, "r") as f:
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

    service = CrystallizeService()
    session_id = service.new_session(network, germ)
    steps = service.run(session_id, max_steps=args.steps, halt_on_stable=True)

    print(f"Crystallized {len(steps)} steps.")
    print(f"\nStep summary:")
    for step in steps:
        mode = step.dominant_mode()
        print(f"  [{step.index:3d}]  S={step.entropy:.4f}  ΔS={step.entropy_delta:+.4f}  "
              f"F={step.free_energy:.4f}  dominant={mode.value if mode else '—'}  "
              f"{'⚡ REGIME CHANGE' if step.regime_change else ''}")

    outfile = args.out or "session.json"
    out = {
        "session_id": session_id,
        "germ_label": germ.label,
        "steps": [
            {
                "index": s.index,
                "entropy": s.entropy,
                "entropy_delta": s.entropy_delta,
                "free_energy": s.free_energy,
                "mode_distribution": s.mode_distribution,
                "regime_change": s.regime_change,
                "simplex_count": len(s.network),
            }
            for s in steps
        ],
    }
    with open(outfile, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSession saved → {outfile}")


def _load_network(path: str):
    """Load a SimplexNetwork from a JSON file produced by `ri ingest`."""
    from core.network import SimplexNetwork
    from core.simplex import Simplex
    from core.term import Term

    with open(path, "r") as f:
        data = json.load(f)

    network = SimplexNetwork()
    for s in data["simplexes"]:
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


def main():
    parser = argparse.ArgumentParser(
        prog="ri",
        description="research-indexer — an individuation machine for texts",
    )
    sub = parser.add_subparsers(dest="command")

    # ingest
    p_ingest = sub.add_parser("ingest", help="Extract a SimplexNetwork from a text file")
    p_ingest.add_argument("source")
    p_ingest.add_argument("--domain", default="sentence",
                          choices=["sentence", "thought", "argument", "work", "corpus"])
    p_ingest.add_argument("--medium", default="plaintext")
    p_ingest.add_argument("--out", default=None)

    # germ
    p_germ = sub.add_parser("germ", help="Detect or supply a germ")
    germ_sub = p_germ.add_subparsers(dest="germ_command")

    p_detect = germ_sub.add_parser("detect")
    p_detect.add_argument("network_file")
    p_detect.add_argument("--min-displacement", type=float, default=0.01)

    p_supply = germ_sub.add_parser("supply")
    p_supply.add_argument("network_file")
    p_supply.add_argument("--label", required=True)
    p_supply.add_argument("--cycle", nargs="+", required=True)
    p_supply.add_argument("--out", default="germ.json")

    # crystallize
    p_crys = sub.add_parser("crystallize", help="Run crystallization from a germ")
    p_crys.add_argument("network_file")
    p_crys.add_argument("--germ", required=True)
    p_crys.add_argument("--steps", type=int, default=50)
    p_crys.add_argument("--out", default=None)

    args = parser.parse_args()

    if args.command == "ingest":
        cmd_ingest(args)
    elif args.command == "germ":
        if args.germ_command == "detect":
            cmd_germ_detect(args)
        else:
            parser.print_help()
    elif args.command == "crystallize":
        cmd_crystallize(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
