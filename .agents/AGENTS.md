## Code Example Execution Instructions
Whenever showing a code example that requires third-party packages or environment setup (e.g., Pydantic), always provide instructions using the `::tabs` Docus component showing how to install dependencies and run the code via `pip`, `uv`, and `poetry`.

Example format:
```markdown
::tabs
::tabs-item{label="pip"}
\`\`\`bash
# Install and run instructions using pip
\`\`\`
::
::tabs-item{label="uv"}
\`\`\`bash
# Install and run instructions using uv
\`\`\`
::
::tabs-item{label="poetry"}
\`\`\`bash
# Install and run instructions using poetry
\`\`\`
::
::
```
