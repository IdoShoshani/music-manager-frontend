
# 🎵 Music Manager

A web application for managing music collections with artists, playlists, and favorites.

## Features
- **Artist Management**: 🎤 Add/delete artists and songs
- **Playlist Creation and Management**: 📀 Organize and manage playlists
- **Favorites List**: ❤️ Mark your favorite songs
- **MongoDB Database**: 💾 Robust data storage
- **REST API Backend**: 🔗 Seamless backend support
- **Web Frontend**: 💻 User-friendly interface

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/username/music-manager.git
    cd music-manager
    ```
2. **Ensure Docker and Docker Compose are installed**.
3. **Run the following command**:
    ```bash
    docker-compose up -d
    ```

### Access the application:
- **Frontend**: [http://localhost](http://localhost)
- **API**: [http://localhost:5000](http://localhost:5000)

## Testing

Run unit tests:
```bash
docker-compose run test
```

## Project Structure
```
music-manager/
├── backend/          # 🛠️ Flask API
├── frontend/         # 🌐 Web interface
└── docker-compose.yml # ⚙️ Docker configuration
```


