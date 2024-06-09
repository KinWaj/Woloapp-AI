"""Main app"""
from app import app  # pylint: disable=W0406

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port='5000')
