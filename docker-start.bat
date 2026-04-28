@echo off
echo ====================================
echo Запуск Digital Buddy через Docker
echo ====================================
echo.

echo Проверка Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker не установлен!
    echo Установите Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo.
echo Построение Docker образа...
docker-compose build

echo.
echo Запуск сервисов...
docker-compose up -d

echo.
echo ====================================
echo Digital Buddy запущен!
echo Откройте: http://localhost:8501
echo ====================================
echo.
echo Для остановки: docker-compose down
echo Для просмотра логов: docker-compose logs -f
pause
