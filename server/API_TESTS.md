## Login

```bash
$loginBody = @{
email = "jane@gmail.com"
password = "jane123"
} | ConvertTo-Json

$tokenResponse = Invoke-RestMethod `    -Method POST`
-Uri "http://127.0.0.1:8000/auth/login" `    -ContentType "application/json"`
-Body $loginBody

$token = $tokenResponse.access_token

$headers = @{
Authorization = "Bearer $token"
}

$token
```

## Verify user

```bash
Invoke-RestMethod `
    -Method GET `
    -Uri "http://127.0.0.1:8000/me" `
    -Headers $headers
```

## Create Repository

```bash
$repoBody = @{
    name = "Test Repo"
    github_url = "https://github.com/jane/test-repo"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method POST `
    -Uri "http://127.0.0.1:8000/repositories/" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $repoBody

```

## Get all repositories

```bash
Invoke-RestMethod `
    -Method GET `
    -Uri "http://127.0.0.1:8000/repositories/" `
    -Headers $headers
```

## Get one repository

```bash
Invoke-RestMethod `
    -Method GET `
    -Uri "http://127.0.0.1:8000/repositories/3" `
    -Headers $headers
```

## Create workflow

```bash

$workflowBody = @{
    name = "PR Review Workflow"
    description = "Review incoming pull requests"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method POST `
    -Uri "http://127.0.0.1:8000/repositories/3/workflows" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $workflowBody

```

## Get all workflows

```bash
Invoke-RestMethod `
    -Method GET `
    -Uri "http://127.0.0.1:8000/repositories/3/workflows" `
    -Headers $headers

```

## Get one worklow

```bash
Invoke-RestMethod `
    -Method GET `
    -Uri "http://127.0.0.1:8000/workflows/1" `
    -Headers $headers
```

## Update workflow

```bash
$workflowUpdate = @{
    description = "Updated workflow description"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method PATCH `
    -Uri "http://127.0.0.1:8000/workflows/1" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $workflowUpdate
```

## Create workflow steps

```bash
$stepBody = @{
    name = "Analyze PR"
    step_type = "ai"
    order = 1
    config = @{
        prompt = "Review PR"
    }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
    -Method POST `
    -Uri "http://127.0.0.1:8000/workflows/1/steps" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $stepBody

```

## Get workflow steps

```bash
Invoke-RestMethod `
    -Method GET `
    -Uri "http://127.0.0.1:8000/workflows/1/steps" `
    -Headers $headers

```

## Update step

```bash
$stepUpdate = @{
    name = "Analyze Pull Request"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method PATCH `
    -Uri "http://127.0.0.1:8000/steps/1" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $stepUpdate
```

## Execute workflow

```bash
Invoke-RestMethod `
    -Method POST `
    -Uri "http://127.0.0.1:8000/workflows/1/run" `
    -Headers $headers
```

## Get workflow run

```bash
Invoke-RestMethod `
    -Method GET `
    -Uri "http://127.0.0.1:8000/workflows/1/runs" `
    -Headers $headers
```

## Get one run

```bash
Invoke-RestMethod `
    -Method GET `
    -Uri "http://127.0.0.1:8000/runs/1" `
    -Headers $headers
```

## Get all step runs for a run

```bash
Invoke-RestMethod `
    -Method GET `
    -Uri "http://127.0.0.1:8000/runs/1/steps" `
    -Headers $headers
```

## Get one step run

```bash
Invoke-RestMethod `
    -Method GET `
    -Uri "http://127.0.0.1:8000/runs/1/steps/1" `
    -Headers $headers
```

## Delete step

```bash
Invoke-RestMethod `
    -Method DELETE `
    -Uri "http://127.0.0.1:8000/steps/1" `
    -Headers $headers
```

## Delete Workflow

```bash
Invoke-RestMethod `
    -Method DELETE `
    -Uri "http://127.0.0.1:8000/workflows/1" `
    -Headers $headers
```
