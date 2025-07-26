# Discord-Bot

A simple Discord bot designed to manage voice channel permissions, currently allowing you to mute and unmute all members in a server voice channel with a single command. More features will be added in the future!

## Features

- **Mute All**: Instantly mute everyone in a selected voice channel.
- **Unmute All**: Instantly unmute everyone in a selected voice channel.
- More functionality coming soon!

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v16.9.0 or newer recommended)
- A Discord account
- A Discord server where you have permission to add bots
- A Discord bot token ([How to get one?](https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dianbrown/Discord-Bot.git
   cd Discord-Bot
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure your bot:**
   - Create a `.env` file in the root directory.
   - Add your Discord bot token:
     ```
     DISCORD_TOKEN=your-bot-token-here
     ```

4. **Run the bot:**
   ```bash
   npm start
   ```

## Usage

Once the bot is running and invited to your server, use the designated command(s) to mute or unmute everyone in a voice channel. Command syntax and details will depend on your bot's command implementation.

Example commands:

- `/muteall` — Mutes all users in your current voice channel.
- `/unmuteall` — Unmutes all users in your current voice channel.

## Contributing

Contributions are welcome! Please open issues or pull requests for suggestions, bug fixes, or new features.

## License

[MIT](LICENSE)

## Roadmap

- [x] Mute all users in a voice channel
- [x] Unmute all users in a voice channel
- [ ] Add more moderation features
- [ ] Add customizable commands
- [ ] Add logging and audit features
