import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../config/api.config';
import { Activity, ActivityCreate } from '../../models/activity.model';
import {
  Project,
  ProjectCreate,
  ProjectDetail,
  ProjectUpdate,
} from '../../models/project.model';

@Injectable({
  providedIn: 'root',
})
export class ProjectService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${API_BASE_URL}/projects`;

  list(): Observable<Project[]> {
    return this.http.get<Project[]>(this.baseUrl);
  }

  getById(projectId: number): Observable<ProjectDetail> {
    return this.http.get<ProjectDetail>(`${this.baseUrl}/${projectId}`);
  }

  create(data: ProjectCreate): Observable<Project> {
    return this.http.post<Project>(this.baseUrl, data);
  }

  update(projectId: number, data: ProjectUpdate): Observable<Project> {
    return this.http.patch<Project>(`${this.baseUrl}/${projectId}`, data);
  }

  delete(projectId: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${projectId}`);
  }

  /** Nested resource: `POST /projects/{id}/activities`. */
  createActivity(
    projectId: number,
    data: ActivityCreate,
  ): Observable<Activity> {
    return this.http.post<Activity>(
      `${this.baseUrl}/${projectId}/activities`,
      data,
    );
  }
}
