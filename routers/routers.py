class MyDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.model_name == 'secondtablebooks':
            return 'mydatabase'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.model_name == 'secondtablebooks':
            return 'mydatabase'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'secondtablebooks':
            return db == 'mydatabase'
        else:
            return db == 'default'
