# Evidencias (capturas)

Coloca aquí las capturas que se muestran en el README principal:

| Archivo | Qué capturar |
|---------|--------------|
| `01-docker-build.png` | `docker build -t sentiment-api .` terminado sin errores |
| `02-docker-run.png` | `docker run --rm -p 8000:8000 sentiment-api` con el log "Application startup complete" |
| `03-swagger.png` | Navegador en `http://localhost:8000/docs` |
| `04-predict-positivo.png` | POST `/predict` con texto positivo → `"label": "positivo"` |
| `05-predict-negativo.png` | POST `/predict` con texto negativo → `"label": "negativo"` |
| `06-tests-passing.png` | `uv run pytest -q` en verde |
| `07-ci-github.png` | Pestaña **Actions** de GitHub con el workflow en verde |
</content>
</invoke>
