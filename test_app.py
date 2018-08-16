from app import app
import json
import unittest

class basicUnitTest(unittest.TestCase):
    def test_index_url(self):
        self.app = app.test_client()
        response = self.app.get("/todo/api/v1.0/tasks")
        self.assertEqual(response.status_code, 200)

    def test_index_url_invalid(self):
        self.app = app.test_client()
        response = self.app.get("/todo/api/v1.0/task")
        self.assertEqual(response.status_code, 404)


    def get_one_task(self, task_id):
        url = "/todo/api/v1.0/tasks/" + str(task_id)
        return self.app.get(url)

    def post_one_task(self, title, description, done):
        return self.app.post(
            "/todo/api/v1.0/tasks",
            data=json.dumps(dict(title=title, description=description, done=done)),
            content_type = 'application/json'
        )

    def update_one_task(self, task_id, title, description, done):
        url = "/todo/api/v1.0/tasks/" + str(task_id)
        return self.app.put(
            url,
            data=json.dumps(dict(task_id = task_id, title=title, description=description, done=done)),
            content_type = 'application/json'
        )

    def delete_task(self, task_id):
        url = "/todo/api/v1.0/tasks/" + str(task_id)
        return self.app.delete(
            url,
            data=json.dumps(dict(task_id = task_id)),
            content_type = 'application/json'
        )

    def test_get_task(self):
        self.app = app.test_client()
        response = self.get_one_task(1)
        self.assertEqual(response.status_code, 200)
        response = self.get_one_task("1")
        self.assertEqual(response.status_code, 200)
        response = self.get_one_task('1')
        self.assertEqual(response.status_code, 200)

    def test_get_task_invalid(self):
        self.app = app.test_client()
        response = self.get_one_task(250)
        self.assertEqual(response.status_code, 500)
        response = self.get_one_task("a")
        self.assertEqual(response.status_code, 404)

    def test_add_task(self):
        self.app = app.test_client()
        response = self.post_one_task("Test case1", "Unit testing case 1", False)
        self.assertEqual(response.status_code, 200)
        response = self.post_one_task("Test case2", "Unit testing case 2", True)
        self.assertEqual(response.status_code, 200)
        response = self.post_one_task("Test case3", "", False)
        self.assertEqual(response.status_code, 200)

    def test_add_task_invalid(self):
        self.app = app.test_client()
        response = self.post_one_task("", "Test case without title", True)
        self.assertEqual(response.status_code, 500)
        response = self.post_one_task("Test case without desc", "", False)
        self.assertEqual(response.status_code, 200)
        response = self.post_one_task("Test case without done", "", "")
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        self.app = app.test_client()
        response = self.update_one_task(1, "new title", "", "")
        self.assertEqual(response.status_code, 200)
        response = self.update_one_task(2, "", "new Desc", "")
        self.assertEqual(response.status_code, 200)
        response = self.update_one_task(3, "", "", True)
        self.assertEqual(response.status_code, 200)

    def test_update_task_invalid(self):
        self.app = app.test_client()
        response = self.update_one_task(500, "new title", "", "")
        self.assertEqual(response.status_code, 500)
        response = self.update_one_task('', "new title", "", "")
        self.assertEqual(response.status_code, 404)

    def test_delete_task(self):
        self.app = app.test_client()
        response = self.delete_task(5)
        self.assertEqual(response.status_code, 200)

    def test_delete_task_invalid(self):
        self.app = app.test_client()
        response = self.delete_task('')
        self.assertEqual(response.status_code, 404)


unittest.main()