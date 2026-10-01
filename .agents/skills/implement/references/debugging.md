# Debugging loop

Use this loop when the cause is not already established:

1. Reproduce the failure reliably.
2. Minimize the reproducer and identify the failing boundary.
3. Gather evidence from logs, state, inputs, and recent changes.
4. Form one falsifiable hypothesis.
5. Run the smallest experiment that can disprove it.
6. Fix the root cause, not the visible symptom.
7. Add regression protection proportional to the risk.
8. Run neighboring checks and remove temporary instrumentation.

Do not stack speculative fixes. After a failed hypothesis, revert its incidental
changes before testing the next one.

