# Privacy Policy

**Taste Graph Generator** (this repository) is a personal, single-user project built and operated by Jessica Kuang. It is not a commercial product or service, and it does not have users other than its own developer running it locally on their own machine.

## What this app is

Taste Graph Generator runs entirely on the user's own computer. It builds a personalized "taste graph" from images and, optionally, listening data the user connects from their own accounts (Pinterest, Spotify, Google Photos, Apple Photos), then renders that graph locally at `localhost:5000`. There is no hosted version, no multi-user login, and no central server operated by anyone.

## What data is accessed and why

When a data source is connected (for example, Pinterest), the app requests read-only access, specifically:
- **Pinterest**: board names and pin images (`boards:read`, `pins:read` scopes), used only to download the images and build an aesthetic profile
- **Spotify**: top artists and genres (`user-top-read` scope), used only to add music-mood descriptors to the taste profile
- **Google Photos / Apple Photos**: photos the user explicitly picks or has favorited, used the same way

No data is written back to any of these platforms. Nothing is posted, modified, or deleted on the user's behalf.

## Where data is stored

All fetched images, OAuth tokens, and generated profile data are written to local folders on the user's own machine (`data/uploads/`, `data/tokens/`, `data/profiles/`) and are excluded from version control via `.gitignore`. None of this data is transmitted to any third-party server, database, or analytics service, with the sole exception of the Anthropic API, which is called to generate descriptive text for the user's own taste profile from the user's own data, and is not used to store or resell that data.

## What is never done with this data

- Nothing is sold, shared, or licensed to any third party
- Nothing is used for advertising or ad targeting
- No data is retained on any server, there is no server, only the user's own local machine

## User control

Because everything lives locally, the user can delete any or all of it at any time by deleting the relevant folder under `data/`, and can revoke any platform's access at any time directly from that platform's own account settings (e.g. Pinterest Settings → Apps, Spotify Account → Apps).

## Contact

This is a personal project. Questions can be raised via a GitHub issue on this repository: https://github.com/jessica-kuang/taste-graph-generator/issues
