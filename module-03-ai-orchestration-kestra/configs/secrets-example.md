# Secrets Management Guide

## What are Secrets?

Secrets are sensitive values that should never be exposed in code or logs:

- API keys
- Database passwords
- OAuth tokens
- Encryption keys
- Personal information

## Storing Secrets Safely

### Option 1: Kestra UI (Recommended for Local Development)

1. Start Kestra: `docker-compose up`
2. Open dashboard: `http://localhost:8080`
3. Navigate to: **Settings → Secrets**
4. Click: **"Add Secret"**
5. Enter:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `your-actual-api-key`
6. Click: **"Save"**

Usage in workflows:
```yaml
auth:
  username: "{{ secret('GEMINI_API_KEY') }}"
```

### Option 2: Environment Variables (Development Only)

```bash
# In terminal before running Kestra
export GEMINI_API_KEY=your-api-key
docker-compose up
```

⚠️ **Security Note**: This is suitable only for local development, not production.

### Option 3: Docker Compose Environment

```yaml
# docker-compose.yml
services:
  kestra:
    environment:
      KESTRA_SECRETS_GEMINI_API_KEY: ${GEMINI_API_KEY}
```

Load from `.env`:
```bash
GEMINI_API_KEY=your-actual-key
```

### Option 4: Production – AWS Secrets Manager

```python
import boto3

client = boto3.client('secretsmanager')

response = client.get_secret_value(
    SecretId='kestra/gemini-api-key'
)

api_key = response['SecretString']
```

### Option 5: Production – HashiCorp Vault

```python
import hvac

client = hvac.Client(url='http://127.0.0.1:8200')

response = client.secrets.kv.v2.read_secret_version(
    path='kestra/gemini-api-key'
)

api_key = response['data']['data']['api_key']
```

### Option 6: Production – Google Cloud Secret Manager

```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()

name = client.secret_version_path(
    "my-project",
    "gemini-api-key",
    "latest"
)

response = client.access_secret_version(request={"name": name})
secret_string = response.payload.data.decode('UTF-8')
```

## Secret Naming Conventions

Use consistent naming for easy management:

```
GEMINI_API_KEY          # LLM API key
DATABASE_PASSWORD       # Database credentials
REDIS_PASSWORD          # Cache credentials
GITHUB_TOKEN            # GitHub API token
SLACK_WEBHOOK_URL       # Slack notifications
AWS_ACCESS_KEY_ID       # AWS credentials
OPENAI_API_KEY          # Alternative LLM
VECTOR_DB_PASSWORD      # Vector database
```

## Rotating Secrets

### When to Rotate

- ✅ Quarterly (regular maintenance)
- ✅ After employee departure
- ✅ If accidentally exposed
- ✅ After security incident
- ✅ When changing providers

### Rotation Process

1. **Create new secret** (keep old one active)
2. **Test new secret** in staging environment
3. **Update configuration** to use new secret
4. **Monitor for errors** during transition
5. **Deactivate old secret** after verification
6. **Document rotation** in audit log

## Accessing Secrets in Workflows

### In HTTP Request

```yaml
tasks:
  - id: api_call
    type: io.kestra.plugin.core.http.Request
    uri: https://api.example.com/endpoint
    auth:
      type: BASIC
      username: "{{ secret('API_KEY') }}"
```

### In Body

```yaml
body: |
  {
    "api_key": "{{ secret('GEMINI_API_KEY') }}"
  }
```

### In Headers

```yaml
headers:
  Authorization: "Bearer {{ secret('API_TOKEN') }}"
```

## Checking Secret Access

### Audit Log (Kestra)

In Kestra UI:
- Settings → Audit Log
- Filter: Secret access
- View: Who accessed what secrets when

### Recommended Audit Trail

```yaml
tasks:
  - id: log_secret_access
    type: io.kestra.plugin.core.log.Log
    message: |
      Secret Access Audit:
      - User: {{ execution.user }}
      - Timestamp: {{ now() }}
      - Secret: GEMINI_API_KEY
      - Flow: {{ execution.flowId }}
      - Status: SUCCESS
```

## Security Checklist

- ☐ Secrets stored in secure service (not code)
- ☐ Access logs enabled
- ☐ Rotation schedule established
- ☐ Separate keys for dev/staging/prod
- ☐ Encryption in transit (HTTPS)
- ☐ Encryption at rest (Kestra encrypted storage)
- ☐ Limited access permissions
- ☐ Monitoring for unusual access patterns
- ☐ Incident response plan ready
- ☐ Team trained on secret handling

## Troubleshooting

### Problem: "Secret not found"

```
Error: Secret 'GEMINI_API_KEY' not found
```

**Solution**:
1. Verify secret name (case-sensitive)
2. Check secret is in correct namespace
3. Reload/restart Kestra
4. Check permissions (user can access secret)

### Problem: "Unauthorized"

```
Error: Unauthorized - invalid credentials
```

**Solution**:
1. Verify secret value is correct
2. Check API key hasn't expired
3. Verify API key has correct permissions
4. Test API key independently

### Problem: "Secret exposed in logs"

```
# BAD - logs the secret!
message: "Using key: {{ secret('GEMINI_API_KEY') }}"
```

**Solution**:
```yaml
# GOOD - safely uses secret without logging it
auth:
  username: "{{ secret('GEMINI_API_KEY') }}"
```

## Best Practices

1. **Never log secrets**: Use `[REDACTED]` in logs
2. **Rotate regularly**: Every 90 days minimum
3. **Different keys per env**: dev ≠ staging ≠ production
4. **Monitor access**: Track who accesses what
5. **Limit scope**: Keys should have minimum required permissions
6. **Use encryption**: TLS for transit, at-rest encryption
7. **Backup strategy**: Recover from accidental deletion
8. **Incident response**: Plan for exposure scenarios

## Additional Resources

- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [AWS Secrets Best Practices](https://docs.aws.amazon.com/secretsmanager/)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [Google Secret Manager](https://cloud.google.com/secret-manager)

---

**Created**: July 3, 2026  
**Last Updated**: July 3, 2026
