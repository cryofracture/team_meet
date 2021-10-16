db.createUser(
    {
        user: "dock_mongo",
        pwd: $MONGO_PASS,
        roles: [
            {
                role: "readWrite",
                db: "<database to create>"
            }
        ]
    }
);