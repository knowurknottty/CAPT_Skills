# Deployment Proof Matrix

Keep these layers distinct:

| Layer | Question | Typical evidence |
|---|---|---|
| Source | What exact revision/config is intended? | commit/tree/config identity; clean diff scope |
| Build | What source actually produced the artifact? | clean build logs; build provenance; artifact digest |
| Package | Is the distributable complete and runnable? | package inspection/install/smoke result |
| Deploy | Where did the artifact go? | pipeline/deployment ID; target environment/project; recorded artifact identity |
| Route/cache | What path reaches it? | origin/custom-domain/preview/DNS/cache probes |
| Runtime | Does the deployed artifact start/serve and perform acceptance behavior? | live route/launch/readiness/interaction evidence |
| Degraded mode | What happens when required dependencies fail? | controlled dependency-failure probes and bounded user/system behavior |
| Rollback/recovery | Can an accepted prior/new state be restored deliberately? | rehearsed rollback/redeploy/restart plus post-recovery acceptance |

A higher layer cannot substitute for a missing lower-layer identity link. “The live UI looks new” does not prove the intended commit is deployed; “deployment succeeded” does not prove runtime readiness.
