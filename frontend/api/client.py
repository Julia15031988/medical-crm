import requests


class ApiClient:
    BASE_URL = "http://localhost:8000/api/v1"

    def __init__(self):
        self.access_token = None
        self.refresh_token = None

    # ==========================
    # AUTH
    # ==========================

    def login(self, email: str, password: str):
        response = requests.post(
            f"{self.BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password,
            },
            timeout=10,
        )

        if response.status_code != 200:
            try:
                raise Exception(response.json()["detail"])
            except Exception:
                raise Exception(response.text)

        data = response.json()

        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]

        return data

    def get_headers(self):
        if not self.access_token:
            return {}

        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    # ==========================
    # PATIENTS
    # ==========================

    def get_patients(self):
        return self._get("/patients/")

    # ==========================
    # DOCTORS
    # ==========================

    def get_doctors(self):
        return self._get("/doctors/")

    # ==========================
    # APPOINTMENTS
    # ==========================

    def get_appointments(self):
        return self._get("/appointments/")

    # ==========================
    # PRIVATE
    # ==========================

    def _get(self, endpoint):
        response = requests.get(
            f"{self.BASE_URL}{endpoint}",
            headers=self.get_headers(),
            timeout=10,
        )

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()

    def create_patient(self, patient_data):
        response = requests.post(
            f"{self.BASE_URL}/patients/",
            json=patient_data,
            headers=self.get_headers(),
            timeout=10,
        )

        if response.status_code != 201:
            raise Exception(response.text)

        return response.json()

    def create_doctor(self, doctor_data):
        response = requests.post(
            f"{self.BASE_URL}/doctors/",
            json=doctor_data,
            headers=self.get_headers(),
            timeout=10,
        )

        if response.status_code != 201:
            raise Exception(response.text)

        return response.json()

    def create_appointment(self, appointment_data):
        response = requests.post(
            f"{self.BASE_URL}/appointments/",
            json=appointment_data,
            headers=self.get_headers(),
            timeout=10,
        )

        if response.status_code != 201:
            raise Exception(response.text)

        return response.json()

api_client = ApiClient()
