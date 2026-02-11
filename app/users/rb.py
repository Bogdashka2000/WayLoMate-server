from datetime import date

class RBUser:
    def __init__ (
        self,
        user_id: int | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        birthday: date | None = None,
        gender: str | None = None, 
        ):
        self.user_id = user_id,
        self.first_name = first_name,
        self.last_name = last_name,
        self.birthday = birthday,
        self.gender = gender

    def to_dict(self) -> dict:
        
        dict_result = {
            "user_id" : self.user_id,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "birthday" : self.birthday,
            "gender" : self.gender
        }

        filtered_dict_result = {key: value for key, value in dict_result.items() if value is not None}
        
        return filtered_dict_result