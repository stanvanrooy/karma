import database


def create_alert():
    alert = database.Alert(
        status='firing',
        startsAt='2019-01-01T00:00:00Z',
        endsAt='',
        generatorURL='http://localhost:8080/api/1/generator/1',
        labels={'alertname': 'TestAlert'},
        annotations={'description': 'Test alert'},
        webhook_id=''
    )
    database.db.session.add(alert)
    database.db.session.commit()
    return alert


def create_note(alert):
    note = database.Note(
        alert_id=alert.id,
        text='Test note',
    )
    database.db.session.add(note)
    database.db.session.commit()


def create_webhook():
    webhook = database.Webhook(
        name = 'TestWebhook',
    )
    database.db.session.add(webhook)
    database.db.session.commit()
    return webhook
