# Atenea Updates Notifications

Very simple Python script to get notified when new documents are uploaded to
Atenea (an instance of Moodle). Makes use of a Gotify server.

## Example `config.json`

The `.json` file with the configuration looks like the following:

```json
{
  "notification_domain": "<gotify-domain>",
  "time_interval": 120,
  "api_token": "<moodle-api-token>",
  "notification_token": "<gotify-token>",
  "course_ids": {
    "56145": "GD",
    "56152": "EDPS"
  }
}
```

## License

The program is licensed under the GNU Affero General Public License version 3 or
later (available [here][agpl]).

## Authors

Alphabetically by last name.

- **Oscar Benedito** - oscar@oscarbenedito.com
- **Ernesto Lanchares** - e.lancha98@gmail.com
- **Ferran López** - flg@tuta.io

[agpl]: <https://www.gnu.org/licenses/agpl-3.0.html> "The GNU General Public License v3.0"
