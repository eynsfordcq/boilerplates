# portainer

## Configuring Gitlab OAuth

### Gitlab Configuration

- Go to Admin -> Applications -> Add New Applications.
- Fill up the details:
  - name: give it any name, e.g. portainer
  - redirect url: the url for where portainer is hosted. e.g. `https://192.168.1.5:9443`
  - trusted: check
  - confidential: check
  - scopes: check: openid, profile, email
- Keep this page, copy the application id and secret.

### Portainer Configuration

- Based on this [Gitlab Documentation](https://docs.gitlab.com/integration/openid_connect_provider/), gitlab supports import OIDC settings from discovery URL.
- Portainer doesn't support, but we'll use this as reference.
- Go to Settings -> Authentication
- Fill up the details:
  - Use SSO: check
  - Automatic user provisioning: check
  - Default team: give it a default team.
  - Provider: select "custom" and fill the followings:
    - client id: application id from gitlab
    - client secret: secret from gitlab
    - authorization url: authorization_endpoint from the discovery url
    - access token url: token_endpoint from the discovery url
    - resource url: userinfo_endpoint from the discovery url
    - redirect url: match the one in gitlab e.g. `https://192.168.1.5:9443`
    - logout url: can leave empty
    - user identifier: "nickname"
    - scopes: "openid profile email"
    - auth style: leave as-is
