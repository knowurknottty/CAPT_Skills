# Interaction and Verification Patterns

Use the current driver/tool schema; names below are conceptual, not a fixed API.

| Situation | Preferred response |
|---|---|
| Initial GUI task | Discover capabilities, bind app/window, capture baseline before input. |
| Stable semantic/AX handle exists | Target that handle; preserve role/label/hierarchy evidence. |
| Only coordinates exist | Require current geometry plus unique visual/structural context; re-capture after layout change. |
| Element/index is stale | Re-capture and resolve again; never reuse a stale index blindly. |
| Click/type appears ineffective | Re-capture; inspect modal/focus/disabled state before retry. |
| App/window changed | Re-bind process/window identity before further input. |
| Consequential submit/send/delete | Verify target first; after action require postcondition plus an independent signal when available. |
| Connection drops after effect request | Treat effect as ambiguous; reconcile actual UI/domain state before retry. |
| Direct structured tool exists | Prefer it over typing into Terminal/editor/browser GUI. |

Do not equate background routing with non-interference unless the active tool proves that behavior. Do not assume a capture is current after any state-changing action.
