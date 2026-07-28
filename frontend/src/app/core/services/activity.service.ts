import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../config/api.config';
import {
  Activity,
  ActivityUpdate,
  ActivityWithIndicators,
} from '../../models/activity.model';

@Injectable({
  providedIn: 'root',
})
export class ActivityService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${API_BASE_URL}/activities`;

  getById(activityId: number): Observable<ActivityWithIndicators> {
    return this.http.get<ActivityWithIndicators>(`${this.baseUrl}/${activityId}`);
  }

  update(activityId: number, data: ActivityUpdate): Observable<Activity> {
    return this.http.patch<Activity>(`${this.baseUrl}/${activityId}`, data);
  }

  delete(activityId: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${activityId}`);
  }
}
