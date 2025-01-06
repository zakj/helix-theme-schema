# helix-theme-schema
> A JSON schema for [Helix][] themes

This allows for a bit of validation and completion when writing themes.
It includes documentation scraped from the [docs][] for some known properties.
Note that taplo's auto-completion does not understand that dotted properties must be quoted!

## Usage

There's no need to have a copy of this repository locally.
Add a [schema directive][] to the top of your theme file:

```toml
#:schema https://zakj.github.io/helix-theme-schema/theme.json
```

[taplo][] is defined as an LSP for helix by default, but you can add this to your `languages.toml` to get formatting:

```toml
[[language]]
name = "toml"
auto-format = true
formatter = { command = "taplo", args = ["fmt", "-"] }
```

With helix's default config, taplo will not validate unless you are in a "workspace", which means a parent directory must contain something like a `.git` repository.
If you see a `this document has been excluded` message from taplo after adding the schema, that's likely the problem.

[helix]: https://helix-editor.com/
[docs]: https://docs.helix-editor.com/themes.html
[schema directive]: https://taplo.tamasfe.dev/configuration/directives.html#the-schema-directive
[taplo]: https://taplo.tamasfe.dev/
