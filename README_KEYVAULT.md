# Key Vault Implementation (Reference Only)

**Note: This approach is not currently used in the project.**

This file is kept for reference in case you want to implement a more complex secret management solution using Azure Key Vault in the future. The current implementation uses Container App environment variables directly for simplicity while maintaining security.

The current implementation:
1. Uses Container App environment variables to store secrets
2. Keeps the architecture simple and maintainable
3. Provides sufficient security for a portfolio project

If you need enterprise-grade secret management in the future, the following documentation explains how to implement Azure Key Vault.

Steps (exact az CLI commands)

1) Create an Azure Key Vault (if you don't have one)

Replace `<vault-name>` and `<location>`.

```powershell
az keyvault create --name rca-tracker-kv --resource-group rca-tracker-rg --location westeurope
```

2) Store the MongoDB connection string as a Key Vault secret

Get the value from your `.env` locally or from the portal. Then:

```powershell
az keyvault secret set --vault-name rca-tracker-kv --name "MONGODB_URL" --value "$(Get-Content .env | Select-String 'MONGODB_URL' | ForEach-Object { $_.ToString().Split('=')[1] })"
```

(Or simply paste the connection string value in place of the `--value` argument.)

3) Assign a system-assigned managed identity to your Container App

This gives the container an identity in Azure so we can grant it access to Key Vault.

```powershell
az containerapp identity assign --name rca-tracker --resource-group rca-tracker-rg
```

This command will return JSON including `principalId` which we need for the next step.

4) Grant Key Vault read permission for secrets to the Container App identity

Replace `<principalId>` with the principalId returned above.

```powershell
az keyvault set-policy --name rca-tracker-kv --object-id <principalId> --secret-permissions get
```

5) Configure your Container App to use the Key Vault secret as an environment variable

Container Apps support referencing Key Vault secrets as environment variables via an ARM-style `valueFrom` that references Key Vault, or by fetching the secret at runtime using the managed identity.

Option A (recommended - reference secret directly in container app configuration):

- In the Azure Portal, open your Container App -> Configuration -> Secrets.
- Add a new secret with the name `MONGODB_URL` and for "Value" choose the option to reference Key Vault (if the portal exposes it). If not available use Option B.

Option B (simpler and explicit): set an environment variable whose value is read at startup by your app using Azure SDK and managed identity. Example (app reads Key Vault secret at runtime):

- Keep the `MONGODB_URL` env var empty in Container App, and in your `app/main.py` detect when env var is missing and then use DefaultAzureCredential to request the secret from Key Vault. (This requires `azure-identity` and `azure-keyvault-secrets` packages.)

6) Redeploy / Restart your container app

Once the managed identity and Key Vault access policy are set, restart the Container App from the portal or with:

```powershell
az containerapp restart --name rca-tracker --resource-group rca-tracker-rg
```

Notes & alternatives
- If you just want to keep things simple for now, you may set the connection string as a Container App secret directly (via Portal) and set it as an environment variable. This is easier but Key Vault + MI is more secure.
- For automation (ARM/Bicep), you can embed the KeyVault reference in the Container App resource definition.

References & next steps
- After you wire Key Vault, update your container app to not source the connection string from `.env` in production. Use `os.getenv('MONGODB_URL')` normally; when deployed Azure will populate it from the secret reference.
- If you want, I can run the above CLI commands for you (create vault, set secret, assign identity, set policy). Say "run keyvault wiring" and I'll execute them.

