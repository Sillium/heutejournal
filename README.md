# heutejournal

Kleine Flask-Anwendung, die verrät, wann das "heute journal" im ZDF läuft. Die Sendezeit wird bei jedem Aufruf aus dem Primetime-Programm von [tvspielfilm.de](https://www.tvspielfilm.de/tv-programm/sendungen/?time=primetime&channel=ZDF) gescrapt (requests + BeautifulSoup). Ist die Sendung nicht zu finden, wird `- - -` geliefert.

Fork von https://github.com/johl/tagesthemen, per [Serverless Framework](https://www.serverless.com/) deployed in eine AWS Lambda (Python 3.8, Region `eu-central-1`) mit API Gateway und CloudFront-Domain.

## Endpunkte

| Pfad     | Antwort                                                             |
|----------|---------------------------------------------------------------------|
| `/`      | HTML-Seite (`templates/index.html`) mit der Uhrzeit                 |
| `/json`  | JSON mit `when`, `searchTerm` und `url`                             |
| `/plain` | Nur die Uhrzeit als Text                                            |

Antworten werden mit `Cache-Control: max-age=300` ausgeliefert.

## Lokal ausführen

```sh
pip install -r requirements.txt
python app.py
```

`applocal.py` ist ein Hilfsskript, das die Zeit einmalig auf der Konsole ausgibt (`python applocal.py`). `.gitpod.yml` führt `npm install && pip install -r requirements.txt` und `python app.py` aus.

## Deployment

Voraussetzungen: Node.js/npm, Python 3, AWS-Zugang und ein Serverless-Account (org `stoerk`, app `sillium-heutejournal`).

```sh
npm install
npx serverless deploy --stage <dev|prod> --param="certificateArn=<ARN>" --param="accountId=<AWS-Account-ID>"
```

- `--stage` ist Pflicht und bestimmt die Domain: `prod` -> `heutejournal.sillium.xyz`, `dev` -> `dev.heutejournal.sillium.xyz`.
- Parameter `certificateArn` (ACM-Zertifikat für CloudFront) und `accountId` (Bucket für CloudFront-Logs) werden in `serverless.yml` referenziert.
- Plugins: `serverless-wsgi`, `serverless-python-requirements`, `serverless-api-cloudfront`.

## Projektstruktur

- `app.py` – Flask-App (Lambda-Handler via serverless-wsgi)
- `applocal.py` – Konsolen-Variante zum Testen
- `templates/index.html` – HTML-Template
- `serverless.yml`, `package.json` – Deployment-Konfiguration
- `scriptable/tagesthemen.js` – iOS-Widget für [Scriptable](https://scriptable.app/) (noch von der Tagesthemen-Vorlage; `apiUrl` zeigt auf `tagesthemen.sillium.org`)
- `shortcut/tagesthemen.shortcut` – iOS-Kurzbefehl (ebenfalls aus der Vorlage)

## Lizenz

Siehe [LICENSE](LICENSE).
