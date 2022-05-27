# jbl-chat
## Usage
With `httpie` installed,
- see all users:

`http -a user:password GET http://127.0.0.1:8000/api/users/`
- send a message to user `<username>`:

`http -a user:password POST http://127.0.0.1:8000/api/conversations/<username>/ content="to <username> with love"`
- see conversation with user `<username>`:

`http -a user:password GET http://127.0.0.1:8000/api/conversations/<username>/`

## Implementation brief
The key entity is that of `Message`. At a high level, `Message`s are grouped in `Conversation`s, which can have multiple `User` participants. This would scale well in case in the future we wanted to implement group conversations, for example. The API endpoint could evolve to allow numerical IDs, which would identify group conversations with multiple participants.

One current shortcoming is the lack of pagination, especially in conversations. Retrieving conversations with many messages might result in performance degradation.

I added an admin area to make some debugging easier, and `api-auth` to use the API with a frontend, but neither is strictly needed for the API to work.

In my first commit I also pushed the `.sqlite` file I generated (even if it was in `.gitignore`). If you want to check that commit out, you can use `user=stefano, password=stefano` in the commands above to play with my implementation without having to generate a dataset - running the server is in that case the only required step. You can use those credentials on my hosted instance. Otherwise, users should be created before using the app.

-----------------------
## Assignment text
Let's set the stage, you're the founder of this new messaging startup and you're building your first product. You know it will change over time with feedback from the rest of the team and users; but you still need to start somewhere.

You're building the backend in Django and your first task is to expose an initial API. With this first release, you want to deliver the following stories.

1. As a user, I want to see all the other users on the platform.
2. As a user, I want to see my conversation with another user
3. As a user, I want to be able to message another user on the platform.

Since this is your startup and your product, that you are going to maintain and extend for some time; it's up to you to setup and use the practices that you think are important to you. And you can use any Python library that you want to use. You're the boss! ;-)

We've setup a Django skeleton project for you + setup Docker. Feel free to use Docker for dev or Python venv for your local development. You can use use any Python libraries you want to use. You do not need to setup any user registration or management, it's fine to create them on the shell and use session authentication for the API. We expect you to deliver your solution as a PR to our public repo.
