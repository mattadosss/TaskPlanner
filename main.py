import webapi

import db_handler

app = webapi.create_flask()

db_handler.create_task(0, "besen", "yesen", "2024-05-08 01:28:54")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
