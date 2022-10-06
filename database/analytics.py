from sqlalchemy import func
from loader import session


class Analytics:
    """
    Класс в котором проходят все статистические расчёты
    И на их основе аналитика
    """

    def __init__(self, group, post):
        self.group = group
        self.post = post

    def get_group_id(self, screen_name):
        """
        Функция принимает название группы и отдаёт её ID
        """
        group_id = session.query(self.post.group_id).join(
            self.group, self.post.group_id == self.group.group_id
        ).filter(
            self.group.screen_name == screen_name).first()
        group_id = group_id[0] if group_id else group_id
        return group_id

    def get_statistic(self, input_data: dict):
        """
        Функция принимает словарь со значениями
        периода времени и группы
        Далее функция возвращает словарь со статистикой
        """
        group_id = self.get_group_id(input_data['name'])

        if group_id:
            # Количество постов за период
            posts = session.query(func.count(self.post.post_id)).filter(
                self.post.group_id == group_id,
                self.post.date >= input_data['date']
            ).first()[0]

            # Количество постов с фото/видео за период
            post_with_photo = session.query(func.count(self.post.post_id)).filter(
                self.post.group_id == group_id,
                self.post.date >= input_data['date'],
                self.post.photo == 'true'
            ).first()[0]

            def get_sum_record(data, query_param):
                parameter = session.query(func.sum(query_param)).filter(
                    self.post.group_id == group_id,
                    self.post.date >= data['date'],
                ).first()[0]
                return parameter

            statistic = {
                'count_post': posts,
                'posts_with_photo': post_with_photo,
                'likes': get_sum_record(input_data, self.post.likes),
                'views': get_sum_record(input_data, self.post.views),
                'comments': get_sum_record(input_data, self.post.quantity_comments),
                'reposts': get_sum_record(input_data, self.post.reposts),
            }
            return statistic
        else:
            return False

    def get_tops_stats(self, input_data: dict, query_param):
        """
        Функция принимает словарь со значением и параметром.
        Ведёт подсчёт максимального параметра и на основе этого
        возвращает ссылку на пост
        """
        group_id = self.get_group_id(input_data['name'])

        max_value_record = session.query(func.max(query_param)).filter(
            self.post.group_id == group_id,
            self.post.date >= input_data['date']
        ).first()[0]
        owner_id = session.query(self.post.owner_id).filter(
            self.post.group_id == group_id,
            self.post.date >= input_data['date'],
            query_param == max_value_record
        ).first()[0]
        post_id = session.query(self.post.post_id).filter(
            self.post.owner_id == owner_id,
            query_param == max_value_record
        ).first()[0]
        return f'https://vk.com/{input_data["name"]}?w=wall{owner_id}_{post_id}'