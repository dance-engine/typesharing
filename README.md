# Type Sharing Tool

This tool generates Python and TypeScript type definitions from a simple YAML input.

## Installation

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
   
2. Install the package using `setup.py`:
   ```bash
   pip install .
   ```
   This will:
    - Install all required Python dependencies.
    - Install TypeScript globally using npm.

3. Verify `typescript` is installed:
   ```bash
   tsc --version
   ```

## Usage

### Generating Types

Run the `main.py` script with a YAML file or folder of YAML files as input:

#### Single YAML File
```bash
python main.py input_types.yaml output/
```

#### Folder of YAML Files
```bash
python main.py input_folder/ output/
```

The generated files will be saved in the specified `output` directory.

### Example YAML Input

```yaml
User:
  type: Object
  properties:
    name:
      type: String
    email:
      type: String
    tags?:
      type: List<String>
      extant: missing
```

### Generated Python Output

```python
from dataclasses import dataclass, field
from typing import Optional, List, Union

class MissingType:
    pass

@dataclass
class User:
    name: str
    email: str
    tags: Union[List[str], MissingType] = MissingType()
```

### Generated TypeScript Output

```typescript
interface User {
    name: string;
    email: string;
    tags?: string[] | null | undefined;
}
```

## Running Tests

To validate the generated files and ensure correctness:

1. Install testing dependencies:
   ```bash
   pip install pytest mypy
   npm install
   ```

2. Run tests:
   ```bash
   pytest tests/test_output_validation.py
   ```

### Optionally
3. Type-check the generated Python file:
   ```bash
   mypy generated_types.py
   ```

4. Validate TypeScript with `tsc`:
   ```bash
   tsc --noEmit generated_types.ts
   ```
