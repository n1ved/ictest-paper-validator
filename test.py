import main
from logger import printsuccess, printfail

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