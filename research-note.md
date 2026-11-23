# Evaluation scope and public example

[Project overview](README.md)

This note records the evidence standard and the conditions needed to interpret the displayed results. The included code checks one release boundary and renders aggregate counts. The full adaptive search experiment requires additional implementation and research assets.

## What counts as a finding

A strict API version hallucination requires evidence that the same actual generated call is invalid in the requested release and valid in another real release. The API must be identified from the call's imports and code context. Arguments cannot be repaired to manufacture the contrast. Functional correctness is assessed separately.

Signature binding establishes some boundaries directly. Other calls require inspection of released implementations or stronger execution evidence. Candidate findings in the experiments were reviewed using call analysis, release evidence, and model-assisted review. Unresolved cases remain visible; the verifier's coverage and possible review errors limit what can be concluded.

The earlier task audit concerned whether calls could distinguish releases. It contained 722 high-confidence sites, of which 636 were assessable and six showed a version distinction. The other 86 sites encountered checker errors. These are properties of the evaluated calls, not a model hallucination rate. The NiceGUI example was selected and checked independently.

## Conditions of the displayed comparison

The November 19, 2026 comparison was the GPT-family endpoint's first full evaluation on a frozen pool of 4,704 distinct API/release-pair keys, following smaller prompt checks. Each strategy received 800 logical test actions with empty starting feedback and no common warm-up. An action could test both release sides; a logical action is not equivalent to one physical model request.

The strategies shared the candidate pool, tested endpoint, and verification setup. Selections were committed before answers for the batch arrived. A strategy received feedback only from the actions it selected; identical selected actions could share execution.

| Strategy | Actions | Distinct verified failures | Unresolved actions |
| --- | ---: | ---: | ---: |
| Original feedback policy | 800 | 166 | 202 |
| Simplified feedback policy | 800 | 82 | 194 |
| Random search | 800 | 65 | 249 |

These are all three arms of this comparison. A confirmed combination of distribution package, actual API, and ordered release pair counts once per strategy. Invalid tasks, serving failures, and other unresolved actions consume their selected budget. Unresolved actions are not treated as confirmed negative outcomes.

The comparison concerns complete search configurations. It does not attribute differences to a single component. It contains one run per configuration, with no statistical significance claim. Physical requests, token use, and cost can differ even when logical action budgets match. The results describe targeted failure discovery under this protocol; they do not establish prevalence in ordinary development or superiority across models.

## Verify the public example

The [NiceGUI call site][nicegui] uses:

```python
Multiprocess(config, target=Server.instance.run, sockets=[sock]).run()
```

The Uvicorn constructor requires `target` in 0.40.0 and rejects it in 0.51.0. From the repository root, use separate environments for the two releases:

```sh
uv run --isolated --with 'uvicorn==0.40.0' python examples/check_uvicorn_binding.py
uv run --isolated --with 'uvicorn==0.51.0' python examples/check_uvicorn_binding.py
```

| Release | With `target` | Without `target` |
| --- | --- | --- |
| 0.40.0 | Accepted | Rejected |
| 0.51.0 | Rejected | Accepted |

The script uses `inspect.signature(...).bind(...)` without constructing a server. It reproduces the constructor-binding boundary, and does not reproduce the recorded model completions or establish whole-program correctness. [0.40.0 source][old] · [0.51.0 source][new]

## Regenerate the displayed result

```sh
uv run scripts/plot_results.py
```

The script declares its Matplotlib dependency, reads [the three aggregate rows](data/search-results.csv), and writes `figures/comparison.png`. It makes no model requests. It can also be run with Python 3.10+ and Matplotlib 3.10.8 installed.

The CSV contains the final counts for the displayed comparison. It does not contain task prompts, generated programs, individual finding identities, or verification records. Regenerating this plot checks the presentation of the aggregates. Independently reassessing findings and repeating the search requires the full research implementation and evidence, which are outside this public artifact.

[nicegui]: https://github.com/zauberzeug/nicegui/blob/4c5375de1d83ba274e5d769ce7caf57293767fcd/nicegui/ui_run.py#L309
[old]: https://github.com/Kludex/uvicorn/blob/0.40.0/uvicorn/supervisors/multiprocess.py
[new]: https://github.com/Kludex/uvicorn/blob/0.51.0/uvicorn/supervisors/multiprocess.py
