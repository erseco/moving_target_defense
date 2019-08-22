## Moving Target Defense

---

GitHub
<br>
@jeffcole

Twitter
<br>
@obscurehobo

---

### What does it mean <br> for an application <br> to be "well-designed?"

---

> From a practical point of view, changeability is the only design metric that matters; code that’s easy to change *is* well-designed.

> **Sandi Metz**

---

#### How do Elixir and Phoenix help us to write <br> easy-to-change applications?

---

#### How can we help ourselves <br> to write easy-to-change <br> Elixir and Phoenix applications?

---

### How do Elixir and Phoenix help?

---

### Controllers

---

```elixir
def create(conn, %{"post" => post_params}) do
  changeset = Post.changeset(post_params)

  case Repo.insert(changeset) do
    {:ok, post} ->
      conn
      |> put_flash(:info, "Post created successfully.")
      |> redirect(to: post_path(conn, :show, post))
    {:error, changeset} ->
      render(conn, "new.html", changeset: changeset)
  end
end
```

@[2, 4]

---

### Ecto

> A database wrapper and <br> integrated query language for Elixir

https://hex.pm/packages/ecto

---

#### Schemas

---

```elixir
use Ecto.Schema

schema "posts" do
  field :title, :string
  field :body, :text
  field :published, :boolean, default: false

  timestamps()
end
```

---

#### You can have *n* schemas per table

---

#### Schemas are data mappers

- From the database to application code |
- From user input to application code |
- From application code to the database |

---

#### Changesets

---

```elixir
import Ecto.Changeset

def changeset(%Post{} = post, attrs) do
  post
  |> cast(attrs, [:title, :published])
  |> validate_required([:title, :published])
end
```

---

#### You can have *n* changesets, <br> one for each use case

---

#### Changesets transform and validate data
- User input into a database schema |
- User input into a form schema... |
  - then into multiple database schemas |
- API responses into schemas |

---

#### Repos

---

```elixir
alias MyApp.{Post, Repo}

Repo.all(Post)

Repo.get!(Post, id)

Repo.insert(changeset)

Repo.update(changeset)

Repo.delete(post)
```

---

#### You interact with your app's repository <br> via its `Repo`

---

#### If you don't see `Repo`, <br> there's no repository interaction happening

---

#### Queries

---

```elixir
import Ecto.Query, only: [from: 2]

from p in Post,
  join: c in Comment, where: c.post_id == p.id
```

---

#### Queries are compiled

Query bugs are surfaced earlier

---

### Ecto Recap

- `Schema`
- `Changeset`
- `Repo`
- `Query`

---

#### Ecto provides a few layers of data abstraction

---

### Back to our controller

---

```elixir
def create(conn, %{"post" => post_params}) do
  changeset =
    Post.changeset(post_params) # Schema and Changeset layers

  case Repo.insert(changeset) do # Repo layer
    {:ok, post} ->
      conn
      |> put_flash(:info, "Post created successfully.")
      |> redirect(to: post_path(conn, :show, post))
    {:error, changeset} ->
      render(conn, "new.html", changeset: changeset)
  end
end
```

@[2-3, 5]

---

#### It's clear which layer you're interacting with

---

### Phoenix 1.3 Contexts

---

#### Contexts are a convention for <br> helping you to design the interactions <br> amongst your data

---

#### Generators

```shell
$ mix phx.gen.html Content Post posts title:string:unique
```

---

```elixir
defmodule MyApp.Content
  def list_posts do # Calls into Repo

  def get_post!(id) do # Calls into Repo

  def create_post(attrs \\ %{}) do # Calls into Repo

  def update_post(%Post{} = post, attrs) do # Calls into Repo

  def delete_post(%Post{} = post) do # Calls into Repo

  def change_post(%Post{} = post) do # Returns a changeset
end
```

@[2]
@[4]
@[6]
@[8]
@[10]
@[12]

---

#### Our controller without a context...

---

```elixir
def create(conn, %{"post" => post_params}) do
  changeset = Post.changeset(post_params)

  case Repo.insert(changeset) do
    {:ok, post} ->
      conn
      |> put_flash(:info, "Post created successfully.")
      |> redirect(to: post_path(conn, :show, post))
    {:error, changeset} ->
      render(conn, "new.html", changeset: changeset)
  end
end
```

@[2, 4]

---

#### With a context, becomes...

---

```elixir
def create(conn, %{"post" => post_params}) do
  case Content.create_post(post_params) do
    {:ok, post} ->
      conn
      |> put_flash(:info, "Post created successfully.")
      |> redirect(to: post_path(conn, :show, post))
    {:error, %Ecto.Changeset{} = changeset} ->
      render(conn, "new.html", changeset: changeset)
  end
end
```

@[2]

---

### Phoenix 1.3 Directory Structure

---

```text
lib
├── my_app
│   └── content
│       ├── content.ex
│       └── post.ex
└── my_app_web
    ├── channels
    ├── controllers
    ├── templates
    └── views
```

@[1]
@[2]
@[3]
@[4]
@[5]
@[2, 6]
@[2, 6-10]

---

### How do these features promote ease-of-change?

---

#### How do Elixir and Phoenix promote <br> ease-of-change?

- Each concept has it's place |
- Code is easy to find |
- Code is declarative |
- It's clear when side-effects are happening |
- Only what we need is provided |

---

### How can we help ourselves?

---

#### Alias all module references to a single atom, <br> and pull them up to the top of each file

---

#### Don't do this

```elixir
def list_posts do
  MyApp.Repo.all(MyApp.Content.Post)
end

# ...
```

---

#### Do this

```elixir
alias MyApp.Repo
alias MyApp.Content.Post

def list_posts do
  Repo.all(Post)
end

# ...
```

---

#### Break up context modules

---

```text
my_app
└── content
    ├── content.ex
    └── post.ex
```

---

```text
my_app
└── content
    ├── content.ex      # Context module
    └── post.ex
```

---

```text
my_app
└── content
    ├── comment.ex
    ├── content.ex      # Context module
    └── post.ex
```

---

```text
my_app
└── content
    ├── author.ex
    ├── comment.ex
    ├── content.ex      # Context module
    └── post.ex
```

---

```text
my_app
└── content
    ├── author.ex
    ├── comment.ex
    ├── content.ex      # Context module
    ├── post.ex
    └── subscription.ex
```

---

```text
my_app
└── content
    ├── author.ex
    ├── comment.ex
    ├── content.ex      # Context module
    ├── post.ex
    ├── subscription.ex
    └── tag.ex
```

---

```elixir
defmodule MyApp.Content
  def list_posts do

  def get_post!(id) do

  def create_post(attrs \\ %{}) do

  def update_post(%Post{} = post, attrs) do

  def delete_post(%Post{} = post) do

  def change_post(%Post{} = post) do

  # All of the above times four...
end
```

@[14]

---

#### A schema can be thought of as a sub-context

---

#### Ecto modules make decent boundary points across schemas

---

```text
my_app
└── content
    ├── comment.ex
    ├── content.ex
    └── post.ex
```

@[3, 5]

---

```text
my_app
└── content
    └── comment
        ├── changeset.ex
        ├── comment.ex   # Schema sub-context module
        ├── query.ex
        ├── repo.ex
        └── schema.ex
    ├── content.ex
    └── post
        ├── ...
```

@[3-8, 10-11]
@[5]

---

#### Sub-contexts need not be persisted entities

---

```text
my_app
└── content
    └── comment
        ├── ...
    ├── content.ex
    └── post
        ├── ...
    └── post_form
        ├── changeset.ex
        ├── post_form.ex # Sub-context module
        └── schema.ex
```

@[3-4, 6-7]
@[8]
@[8-11]

---

#### Don't get carried away

---

### Where did these new ideas come from?

---

### Where did these ~~new~~ ideas come from?

---

![Domain Driven Design](assets/domain-driven-design.jpg)

---

### Domain Driven Design

Eric Evans

- Layered Architecture |
- Entities |
- Modules |
- Repositories |
- Making Implicit Concepts Explicit |
- Side-Effect-Free Functions |
- Declarative Design |
- Refactoring Toward Deeper Insight |
- Bounded Context |
- Minimalism |

---

![Domain Driven Design Quickly](assets/domain-driven-design-quickly.jpg)

https://www.infoq.com/minibooks/domain-driven-design-quickly

---

¿Alguna pregunta?

---

Gracias por su atención
