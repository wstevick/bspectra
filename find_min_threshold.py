#!/usr/bin/env python3
import os
import subprocess

with open("./threshold-test.egsinp.template") as f:
    template = f.read()


for template_var in ["TEMPLATE_VAR_AE", "TEMPLATE_VAR_AP"]:
    # binary search
    test_value = 1  # assume that the minimum for the minimum thresholds will be below this
    step_by = test_value
    for step in range(100):
        step_by /= 2

        fname = f"temp-{os.getpid()}-{step}-{template_var}.egsinp"
        with open(fname, "w") as f:
            f.write(
                template.replace(
                    template_var, str(test_value - step_by)
                ).replace("TEMPLATE_VAR_", "1 # ")
            )

        try:
            subprocess.run(
                ["bspectra", "-i", fname],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            test_value -= step_by
        except subprocess.CalledProcessError as e:
            print("err", e.returncode)

        print(test_value, step_by)

    print(template_var, test_value)
