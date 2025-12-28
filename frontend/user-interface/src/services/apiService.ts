export interface PersonCreate {
  first_name: string;
  last_name: string;
}

export interface PersonResponse {
  id: string;
  first_name: string;
  last_name: string;
  full_name: string;
  date_created: string;
}

export interface UploadImageResponse {
  message: string;
  person_id: string;
  first_name: string;
  last_name: string;
  filename: string;
}

export interface FaceRecognitionResponse {
  success: boolean;
  person_id?: string;
  full_name?: string;
  confidence?: number;
  message: string;
}

export interface AttendanceMarkResponse {
  success: boolean;
  person_id?: string;
  full_name?: string;
  timestamp?: string;
  message: string;
}

export interface AttendanceRecord {
  id: string;
  person_id: string;
  full_name: string;
  timestamp: string;
}

class ApiService {
  private baseUrl: string;
  private apiPrefix: string;

  constructor(baseUrl: string = 'http://localhost:8000', apiPrefix: string = '/api/v1') {
    this.baseUrl = baseUrl;
    this.apiPrefix = apiPrefix;
  }

  private getUrl(endpoint: string): string {
    return `${this.baseUrl}${this.apiPrefix}${endpoint}`;
  }

  // Person Management APIs
  async createPerson(data: PersonCreate): Promise<PersonResponse> {
    const response = await fetch(this.getUrl('/persons/'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Failed to create person: ${response.statusText}`);
    }

    return response.json();
  }

  async getAllPersons(): Promise<PersonResponse[]> {
    const response = await fetch(this.getUrl('/persons/'));

    if (!response.ok) {
      throw new Error(`Failed to get persons: ${response.statusText}`);
    }

    return response.json();
  }

  async getPerson(personId: string): Promise<PersonResponse> {
    const response = await fetch(this.getUrl(`/persons/${personId}`));

    if (!response.ok) {
      throw new Error(`Failed to get person: ${response.statusText}`);
    }

    return response.json();
  }

  async updatePerson(personId: string, data: PersonCreate): Promise<PersonResponse> {
    const response = await fetch(this.getUrl(`/persons/${personId}`), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Failed to update person: ${response.statusText}`);
    }

    return response.json();
  }

  async deletePerson(personId: string): Promise<void> {
    const response = await fetch(this.getUrl(`/persons/${personId}`), {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`Failed to delete person: ${response.statusText}`);
    }
  }

  async getPersonImage(personId: string): Promise<string> {
    const response = await fetch(this.getUrl(`/persons/${personId}/image`));

    if (!response.ok) {
      if (response.status === 404) {
        return ''; // No image available
      }
      throw new Error(`Failed to get person image: ${response.statusText}`);
    }

    const blob = await response.blob();
    return URL.createObjectURL(blob);
  }

  async updatePersonImage(personId: string, image: File): Promise<void> {
    const formData = new FormData();
    formData.append('image', image);

    const response = await fetch(this.getUrl(`/persons/${personId}/image`), {
      method: 'PUT',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to update person image');
    }
  }

  // Face Recognition APIs
  async uploadPersonImage(
    image: File,
    firstName: string,
    lastName: string
  ): Promise<UploadImageResponse> {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('first_name', firstName);
    formData.append('last_name', lastName);

    const response = await fetch(this.getUrl('/face-recognition/upload'), {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to upload image');
    }

    return response.json();
  }

  async recognizeFace(image: File): Promise<FaceRecognitionResponse> {
    const formData = new FormData();
    formData.append('image', image);

    const response = await fetch(this.getUrl('/face-recognition/recognize'), {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to recognize face');
    }

    return response.json();
  }

  // Attendance APIs
  async markAttendanceByFace(image: File): Promise<AttendanceMarkResponse> {
    const formData = new FormData();
    formData.append('image', image);

    const response = await fetch(this.getUrl('/attendance/mark/face'), {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to mark attendance');
    }

    return response.json();
  }

  async markAttendanceManual(personId: string): Promise<AttendanceMarkResponse> {
    const response = await fetch(this.getUrl(`/attendance/mark/manual/${personId}`), {
      method: 'POST',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to mark attendance');
    }

    return response.json();
  }

  async getTodayAttendance(): Promise<AttendanceRecord[]> {
    const response = await fetch(this.getUrl('/attendance/today'));

    if (!response.ok) {
      throw new Error(`Failed to get attendance: ${response.statusText}`);
    }

    return response.json();
  }

  async getAttendanceByDate(date: string): Promise<AttendanceRecord[]> {
    const response = await fetch(this.getUrl(`/attendance/date/${date}`));

    if (!response.ok) {
      throw new Error(`Failed to get attendance: ${response.statusText}`);
    }

    return response.json();
  }

  async getPersonAttendance(
    personId: string,
    startDate?: string,
    endDate?: string
  ): Promise<AttendanceRecord[]> {
    let url = this.getUrl(`/attendance/person/${personId}`);
    const params = new URLSearchParams();

    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);

    if (params.toString()) {
      url += `?${params.toString()}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Failed to get attendance: ${response.statusText}`);
    }

    return response.json();
  }

  async exportTodayAttendanceCSV(): Promise<Blob> {
    const response = await fetch(this.getUrl('/attendance/export/today'));

    if (!response.ok) {
      throw new Error(`Failed to export attendance: ${response.statusText}`);
    }

    return response.blob();
  }

  async exportAttendanceCSVByDate(date: string): Promise<Blob> {
    const response = await fetch(this.getUrl(`/attendance/export/date/${date}`));

    if (!response.ok) {
      throw new Error(`Failed to export attendance: ${response.statusText}`);
    }

    return response.blob();
  }
}

// Export singleton instance
export const apiService = new ApiService();
