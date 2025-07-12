import main
from utils.logger import printsuccess, printfail
def runall():
    print("[format papers]")
    total_pass = True
    results = []
    for i in range(0,3):
        res = main.main("papers/" + str(i) + ".pdf", log=True)
        print("Paper " + str(i) + ":",end=" ")
        total_pass = total_pass and res
        results.append(res)
        printsuccess("Passed","") if res else printfail("Failed","")

    print("[valid paper]")
    total_pass_valid = True
    results_val = []
    for i in range(1,8):
        res = main.main("papers/valid/" + str(i) + ".pdf", log=True)
        print("Paper " + str(i) + ":",end=" ")
        total_pass_valid = total_pass_valid and res
        results_val.append(res)
        printsuccess("Passed","") if res else printfail("Failed","")

    print("[invalid paper]")
    total_pass_invalid = False
    results_inv = []
    for i in range(1,3):
        res = main.main("papers/invalid/" + str(i) + ".pdf", log=True)
        print("Paper " + str(i) + ":",end=" ")
        total_pass_invalid = total_pass_invalid or res
        results_inv.append(res)
        printsuccess("Passed","") if res else printfail("Failed","")


    print("\n[summary][demos]")
    print(f"Total papers: {len(results)}")
    print(f"Results: {results}")
    print(f"Verdict: {'Pass' if total_pass else 'Fail'}")

    print("\n[summary][valid papers]")
    print(f"Total valid papers: {len(results_val)}")
    print(f"Results: {results_val}")
    print(f"Verdict: {'Pass' if total_pass_valid else 'Fail'}")

    print("\n[summary][invalid papers]")
    print(f"Total invalid papers: {len(results_inv)}")
    print(f"Results: {results_inv}")
    print(f"Verdict: {'Fail' if total_pass_invalid else 'Pass'}")

    return "Ran ALL"

# imporve a main function to handle terminal arguments if all run everything , if valid run valid papers, if invalid run invalid papers and if demo run demo papers if none of these run the argument as a paper
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run paper format validation.")
    parser.add_argument('--demo', action='store_true', help="Run demo papers")
    parser.add_argument('--valid', action='store_true', help="Run valid papers")
    parser.add_argument('--invalid', action='store_true', help="Run invalid papers")
    parser.add_argument('--all', action='store_true', help="Run all papers")
    parser.add_argument('--paper', type=str, help="Path to a specific paper to validate")

    args = parser.parse_args()

    if args.demo:
        main.main("papers/demo.pdf", log=True)
    elif args.valid:
        for i in range(1, 8):
            main.main(f"papers/valid/{i}.pdf", log=True)
    elif args.invalid:
        for i in range(1, 3):
            main.main(f"papers/invalid/{i}.pdf", log=True)
    elif args.paper:
        main.main(args.paper, log=True)
    elif args.all:
        runall()
    else:
        print("No valid argument provided. Use --demo, --valid, --invalid or --paper <path>")