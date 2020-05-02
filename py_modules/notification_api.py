import os
import plyer
import configuration


def notify(title, body):
    current_configuration = configuration.get_current()
    assets_location = current_configuration.assets_location
    app_icon = os.path.join(assets_location, 'icon.ico')
    plyer.notification.notify(
        title='<b>' + title + '<\b>',
        message=body,
        app_icon=app_icon,
        timeout=10,  # seconds
    )
