# 🗃️ PydanticStorage

A lightweight, extensible, and fully type-safe data storage system built with **Pydantic** and modern Python. Initially file-based (JSON), it's designed to support multiple backends like CSV, SQL, and more. It enables persistent storage of Pydantic models, auto-generated IDs, metadata, uniqueness constraints, partial updates, and structured storage with a real-world schema.

## 🚀 Features

* ✅ JSON-based file storage for Pydantic models
* 🔐 Unique field constraint (e.g., prevent duplicate emails)
* 🆔 Auto ID assignment starting from `1`
* 🧩 Partial & full record updates
* 🗂️ Structured schema with `metadata` + `records`
* 🧹 Methods like `filter`, `exists`, `count`, `clear`, `create`, `bulk_create`, etc.
* 📦 Metadata support

## 📦 Installation

Install the package using your preferred Python package manager:

### Using `uv`

```bash
uv add pydantic-storage
```

### Using `pip`

```bash
pip install pydantic-storage
```

## 🧠 Usage

### 1. Define your Pydantic model

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int | None = None
    name: str
    email: str
```

### 2. Initialize Storage

```python
from pydantic_storage import JsonFileStorage

store = JsonFileStorage(
    model=User,
    file_name="users.json",
    unique_by=["email"],  # Optional: default is ['id']
    metadata={  # Optional
        "version": "1.0.0",
        "title": "User Store",
        "description": "Stores user info",
    }
)
```

### 3. Create Records

```python
store.create(User(name="Alice", email="alice@example.com"))
store.create(User(name="Bob", email="bob@example.com"))
```

### 4. Get or Filter Records

```python
user = store.get("email", "alice@example.com")
users = store.filter(lambda user: user.name.startswith("A"))
```

### 5. Update Records

```python
# Full update using function
store.update("id", 1, lambda user: user.model_copy(
    update={"email": "new@example.com"}
))

# Partial update
store.update_partial("id", 2, {"name": "Robert"})
```

### 6. Delete or Clear all Records

```python
store.delete("email", "bob@example.com")
store.clear()
```

### 7. Bulk Create

```python
store.bulk_create([
    User(name="Charlie", email="charlie@example.com"),
    User(name="Alice", email="alice@example.com")  # Skipped if duplicate
])
```

## 📁 JSON Structure Example

```json
{
  "metadata": {
    "version": "1.0.0",
    "title": "User Store",
    "description": "Stores user info",
    "storage": {
        "type": "file",
        "encryption": "none"
    },
    "timestamps": {
        "created_at": "2025-07-01T15:30:00Z",
        "updated_at": "2025-07-01T15:45:23Z"
    }
  },
  "records": {
    "1": { 
        "id": 1, 
        "name": "Alice", 
        "email": "alice@example.com" 
    },
    "2": { 
        "id": 2,
        "name": "Bob",
        "email": "bob@example.com"
    }
  }
}
```

## ❗ Exceptions

* `DuplicateEntryError`: Raised when uniqueness is violated on `create`.
* `ValidationError`: Raised if an action violates the model schema.

## 🧪 Testing

Run tests with:

```bash
pytest tests
```

Covers record creation, uniqueness, updates, deletions, and metadata.

## 🛠️ Planned Features

* 🔒 Optional encryption
* 📦 Export/import to CSV, SQLite
* 🕒 Automatic backups
* 🧪 Pytest-based suite
* 📊 Schema evolution support

## 🤝 Contributing

Contributions are welcome! Please open an issue or PR for any improvements.

## 📄 License

MIT License. See the LICENSE file for details.

## 👤 Author

For questions or assistance, contact **Shailesh** at [shaileshpandit141@gmail.com](mailto:shaileshpandit141@gmail.com).
