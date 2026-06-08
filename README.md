# Conversational AI Uho Simulation — Flask Edition

> ⚠️ This is a concept demo using a fixed log.
>
> This project is a visual storyboard demo to illustrate the idea of conversational intervention.
> It does not analyze real conversations or diagnose/detect AI dependency.
> The drift / friction / intervention values shown are fixed values for explanatory purposes only.

---

## Directory Structure

```
uho-simu/
├── app.py                  # Flask routing (debug=True for development)
├── metrics.py              # drift/friction calculation logic (for future use; not yet connected)
├── requirements.txt
├── data/
│   ├── __init__.py         # Python package init
│   └── demo_log.py         # Fixed log data (UhoState dataclass, 20 turns)
├── static/
│   ├── app.css             # Stylesheet
│   ├── app.js              # Frontend logic
│   └── vendor/
│       └── chart.umd.js    # Chart.js 4.4.1 local copy (no CDN required)
└── templates/
    └── index.html          # Jinja2 template (skeleton only)
```

## Getting Started

```bash
python -m pip install -r requirements.txt
python app.py
# → http://127.0.0.1:5000
```

## External Dependencies

| Library | Version | Location | Purpose |
|---------|---------|----------|---------|
| Flask | >=3.0 | pip | Web server |
| Chart.js | 4.4.1 | static/vendor/ | Bundled as fallback. Current rendering uses standard canvas. |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Main UI |
| GET | `/api/log` | Returns all 20 turns as a JSON array |
| GET | `/api/turn/<index>` | Fetches a single turn by zero-based index |

## What This Demo Does / Does Not Do

| Does | Does Not Do |
|------|-------------|
| Visualizes the flow of intervention using a fixed scenario | Analyze or diagnose real conversations |
| Illustrates the concepts of U_fast / U_slow / friction / drift | Measure these values in real time |
| Controls the display timing of disclosure / intervention | Have the AI make actual intervention decisions |

## Future Extension: Moving u_fast / u_slow to 2D Vectors

`metrics.py` is designed to accept both scalars and vectors.
When `u_fast` / `u_slow` are changed to `list[float]` of `[emotion, desire]`,
only the internals of `compute_metrics()` need to be replaced.

```python
# Before (current)
u_fast: float        # 0.36
u_slow: float        # 0.195

# After (future)
u_fast: list[float]  # [emotion, desire] e.g. [0.30, 0.18]
u_slow: list[float]  # [emotion, desire] e.g. [0.18, 0.12]
```

## Current Status

In this version, the priority is on how concepts are presented, not on the validity of the calculation model.
`drift` / `friction` are explanatory values within the fixed log and are not estimated by a mathematical model.

## Development Notes

`app.run(debug=True, port=5000)` in `app.py` is a local development setting.

For public environments, set `debug=False` or use a WSGI server (gunicorn / waitress, etc.).

## Notes
- `Chart.js` is bundled as a fallback. Current rendering uses standard canvas.
- The output of `metrics.py` is not yet reflected in the UI. Integration into `/api/log` is planned for the vector migration.

## Disclaimer

This software is a prototype for research, education, and explanatory purposes.

In its current implementation, it is intended to:

- Play back a fixed scenario
- Visualize the concept of conversational intervention
- Display drift / friction for explanatory purposes

It does **not**:

- Diagnose actual AI dependency
- Estimate psychological states
- Perform real-time conversation analysis
- Make medical or psychological determinations
