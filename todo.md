 ### Encourage Better-Than-Copy Ideal Planning (While Allowing Copy)

  Summary

  - Keep the current data path: task_id resolves to plans_mini/.../task_*.json, and reasoning_chain_text remains file-backed canonical
    context.
  - Update plan_ideal instructions/docstrings so the agent is explicitly told: copying the chain is allowed, but producing a clearer/more
    executable plan is preferred.
  - Add a new plan-ideal skill and load it only for agent_management=ideal.

  Current Reasoning-Chain Ingestion

  - task_context is built in worker code with task_id and passed into the agent.
  - Ideal-mode setup stores that context in plan_store and search_ideal.
  - plan_store.load_plan_for_context() resolves task_id to plans_mini and loads dataset_sequence + reasoning_chain_text.
  - plan_ideal() injects the loaded chain into agent.system_prompt under ## IDEAL PLAN.
  - search_ideal() uses the same loaded plan to enforce one-dataset-per-call sequence order.

  Implementation Changes

  - In strands_evaluation/tools/external/ideal/plan_ideal.py:

  1. Update module docstring and plan_ideal docstring to clearly state: reasoning chain is planning context; copied phrasing is acceptable;
     improved executable planning is preferred.
  2. Replace the current “do not just copy” directive with explicit preference language:

  - “You may copy chain steps if accurate.”
  - “Prefer improving specificity: concrete tool actions, verification checks, and step outputs.”

  3. Keep current behavior intact:

  - File-backed load_plan_for_context()
  - Ignored manual plan_text input
  - System prompt mutation (## IDEAL PLAN) and return message flow.

  4. Keep inject_reasoning_chain_prompt exported but update its docstring wording to match the same preference policy.

  - Add strands_evaluation/tools/skills/plan-ideal/SKILL.md:

  1. Metadata:

  - name: plan-ideal
  - description focused on ideal-mode planning from reasoning-chain context.

  2. Rules:

  - Call plan_ideal first in ideal management runs.
  - Generate a numbered execution plan grounded in chain + dataset order.
  - Copying is allowed when exact, but refinement is recommended.

  3. Required plan quality:

  - explicit verification/computation step per item
  - concrete tool intention per step
  - replan trigger when evidence conflicts with chain assumptions.
  - In strands_evaluation/agent_with_mode.py:

  1. Keep all mode/tool behavior unchanged.
  2. Change skill list selection under enable_skills:

  - If active management mode is ideal, load:
      - strands_evaluation/tools/skills/plan-ideal
      - strands_evaluation/tools/skills/discover-data
      - strands_evaluation/tools/skills/query-data
  - Otherwise keep current planning skill (plan-agent) plus existing data skills.

  3. Implement this with an explicit local planning_skill_path chosen from the resolved management mode, so wiring is deterministic and
     testable.

  Test Plan

  - Update test/test_plan_ideal_file_backed.py:

  3. Assert directive text now contains “copy allowed / improvement preferred” semantics.

  - Update test/test_mode_wrapper.py:

  1. Assert ideal management still exposes plan_ideal + summarize_context.

  - Run targeted tests:

  1. python -m unittest discover -s test -p 'test_plan_ideal_file_backed.py'
  2. python -m unittest discover -s test -p 'test_mode_wrapper.py'
  3. python -m unittest discover -s test -p 'test_search_ideal.py'

  Assumptions

  - No signature change to plan_ideal in this pass.
  - No fallback to task_context["reasoning_chain"]; missing/invalid plans_mini data continues to fail fast.
  - search_ideal sequencing semantics remain unchanged.