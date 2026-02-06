import unittest
from main import app, db, RPAProject

class RPATestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_load(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'RPA Tracker', response.data)

    def test_create_project(self):
        response = self.app.post('/create', data={
            'project_name': 'Test Project',
            'developer_name': 'Test Dev',
            'status': 'Új',
            'arrival_date': '2023-10-27',
            'requestor': 'Test Requestor',
            'percentage': 0,
            'description': 'Test Description'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Projekt sikeresen l', response.data)

        with app.app_context():
            project = RPAProject.query.first()
            self.assertIsNotNone(project)
            self.assertEqual(project.project_name, 'Test Project')
            self.assertEqual(project.description, 'Test Description')

if __name__ == '__main__':
    unittest.main()
