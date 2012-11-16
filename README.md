django-gcm
==========

Djanglo GCM uses Google Cloud Messaging to send push notification to Android devices


Installation
-----------------

Add `gcm` to `INSTALLED_APPS` in your settings file.

Add a url pattern to your `urls.py` file

```python
urlpatterns = patterns('',
    ...
    url(r'^data/gcm/', include('gcm.urls')),
    ...
)
```

Add `GCM_APIKEY` to your settings file.

```python
GCM_APIKEY = "my-api-key-here"
```