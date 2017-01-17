title: Typus API
published: 2017-01-16

# API

[Typus][typus] is an open-source project.
Anyone running Python may install it localy for the best experience and performance.

You are welcome to use this service for any purpose being informed that it runs under a tiny private VPS and may not guarantee instant response.

Otherwise, check out [installation instructions][docs].

## Important

This API doesn't store any inputs. Feel free to browse it's [source][website] before usage.

---

## Usage

- Request url is `https://byashimov.com/typus/api/v1/`
- The only acceptable method is `POST`
- Response type is `JSON`
- Available params: `text`, `lang`, `escape_phrases`

### text

The only **required** field.  
Should have length between the range `(3, 42000)`.

    :::bash
    $ curl --data "text='foo'" https://byashimov.com/typus/api/v1/
    {
      "text": "\u201cfoo\u201d"
    }

### lang

Available values: `en` and `ru`.
    
    :::bash
    $ curl --data "text='foo'&lang=ru" https://byashimov.com/typus/api/v1/                  
    {
      "text": "\u00abfoo\u00bb"
    }

### escape_phrases

Phrases not to be proceeded, comma separated: `(c), (r)`. To pass a comma within a phrase, just escape it with a backslash:

    :::bash
    $ curl --data "text='(c), (r) (tm) (c) (r)&escape_phrases=(c)\, (r), (tm)" http://127.0.0.1:5000/typus/api/v1/ 
    {
      "text": "(c), (r) (tm) \u00a9\u00ae"
    }

We have two pairs here: `(c), (r)` and `(tm)`. So only last two elements had been proceed.

## Handling errors

If anything went wrong, API returns `422` status code with a dictionary of verbose error messages.

    :::bash
    $ curl -X POST http://127.0.0.1:5000/typus/api/v1/ 
    {
      "errors": {
        "text": [
          "This field is required."
        ]
      }
    }


[typus]: https://github.com/byashimov/typus
[docs]: http://py-typus.readthedocs.io/en/latest/#installation
[website]: https://github.com/byashimov/website