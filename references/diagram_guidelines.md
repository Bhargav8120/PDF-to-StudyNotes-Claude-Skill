# Diagram guidelines

## Select a visual only when it adds explanatory value

| Content pattern | Preferred representation |
|---|---|
| Ordered procedure or algorithm | Flowchart |
| Components and dependencies | Block/component diagram |
| Messages exchanged over time | Sequence diagram |
| Lifecycle or protocol states | State diagram |
| Categories and containment | Tree/hierarchy |
| Alternatives and trade-offs | Comparison table |
| Quantitative relationship | Chart with labelled axes |
| Timeline | Timeline |

## Mermaid templates

### Flowchart

```mermaid
flowchart TD
    A[Input] --> B{Condition}
    B -->|Yes| C[Action]
    B -->|No| D[Alternative]
    C --> E[Output]
    D --> E
```

### Sequence diagram

```mermaid
sequenceDiagram
    participant A as Sender
    participant B as Receiver
    A->>B: Request
    B-->>A: Response
```

### State diagram

```mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> Running: scheduled
    Running --> Ready: preempted
    Running --> Blocked: waits for I/O
    Blocked --> Ready: I/O complete
    Running --> [*]: exits
```

### Component diagram

```mermaid
flowchart LR
    U[User] --> API[API]
    API --> S[Service]
    S --> DB[(Database)]
```

These are generic patterns only. Replace nodes and relationships with facts grounded in the source. Do not use a template's sample relationships as facts about the PDF.
