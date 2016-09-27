from django.db import models

class SMModelManager(models.Manager):
    search_key = ()
    default_record = {}

    def __init__(self):
        super(SMModelManager, self).__init__()

    def _validate_json(self, json_str):
        # todo mark as this modification may cause some issue
        if isinstance(json_str, dict):
            return json_str

        if not isinstance(json_str, str):
            raise ValueError("'json' is not a str object.")
        return eval(json_str)

    def get_from_json(self, json=str, key=None):
        dict_obj = self._validate_json(json)

        search_key = key and key or self.search_key
        search_dict = {name: value for name, value in dict_obj.items() if name in search_key}

        if search_dict.__len__() != search_key.__len__():
            for field_name in search_key:
                if not search_dict.get(field_name, None):
                    # pass
                    raise ValueError("Can't find key field '%s' in json." % field_name)

        model_obj = self.model()

        for field_name, field_value in search_dict.items():
            if model_obj.is_foreignkey_field(field_name):
                if isinstance(field_value, dict):
                    field_model = model_obj.get_field_model(field_name)
                    try:
                        search_dict[field_name] = field_model.objects.get_from_json(str(field_value))
                    except field_model.DoesNotExist:
                        raise self.model.DoesNotExist

        return self.get(**search_dict)

    def create_from_json(self, json=str):
        dict_obj = self._validate_json(json)
        obj = self.model(**dict_obj)
        obj.save()
        return obj

    def update_from_json(self, json=str, key=None):
        dict_obj = self._validate_json(json)
        obj = self.get_from_json(json, key)
        params = obj.extract_params(**dict_obj)
        for k, v in params.items():
            setattr(obj, k, v)

        try:
            with transaction.atomic(using=self.db):
                obj.save(using=self.db)
            return obj
        except AttributeError:
            obj.save(using=self.db)
            return obj

    def get_or_create_from_json(self, json, key=None):
        try:
            obj = self.get_from_json(json, key)
            created = False
            return obj, created
        except self.model.DoesNotExist:
            obj = self.create_from_json(json)
            created = True
            return obj, created

    def update_or_create_from_json(self, json, key=None):
        try:
            obj = self.get_from_json(json, key)
        except self.model.DoesNotExist:
            obj = self.create_from_json(json)
            return obj, True  # 'True' means record created

        dict_obj = self._validate_json(json)
        params = obj.extract_params(**dict_obj)
        for k, v in params.items():
            setattr(obj, k, v)

        try:
            with transaction.atomic(using=self.db):
                obj.save(using=self.db)
            return obj, False  # 'False' means updated not created
        except AttributeError:
            obj.save(using=self.db)
            return obj, False

    def get_or_create_default(self):
        # try:
        #     model_obj = self.get_from_json(str(self.default_record))
        # except self.model.DoesNotExist:
        #     model_obj = self.model(**self.default_record)
        #     model_obj.save()
        # return model_obj
        return self.get_or_create_from_json(str(self.default_record))