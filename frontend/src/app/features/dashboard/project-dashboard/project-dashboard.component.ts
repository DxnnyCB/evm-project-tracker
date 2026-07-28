import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, ViewChild, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ActivityService } from '../../../core/services/activity.service';
import { ProjectService } from '../../../core/services/project.service';
import {
  ActivityFormComponent,
  ActivityFormSaveEvent,
} from '../../activities/activity-form/activity-form.component';
import { ActivityTableComponent } from '../../activities/activity-table/activity-table.component';
import { ConsolidatedPanelComponent } from '../../activities/consolidated-panel/consolidated-panel.component';
import { ActivityWithIndicators } from '../../../models/activity.model';
import { ProjectDetail } from '../../../models/project.model';

@Component({
  selector: 'app-project-dashboard',
  imports: [
    RouterLink,
    ConsolidatedPanelComponent,
    ActivityTableComponent,
    ActivityFormComponent,
  ],
  templateUrl: './project-dashboard.component.html',
  styleUrl: './project-dashboard.component.css',
})
export class ProjectDashboardComponent implements OnInit {
  @ViewChild(ActivityFormComponent) private activityForm?: ActivityFormComponent;

  private readonly route = inject(ActivatedRoute);
  private readonly projectService = inject(ProjectService);
  private readonly activityService = inject(ActivityService);

  project: ProjectDetail | null = null;
  activityToEdit: ActivityWithIndicators | null = null;
  loading = false;
  savingActivity = false;
  errorMessage: string | null = null;
  private projectId: number | null = null;

  ngOnInit(): void {
    const rawId = this.route.snapshot.paramMap.get('projectId');
    const projectId = rawId ? Number(rawId) : NaN;
    if (!Number.isInteger(projectId) || projectId <= 0) {
      this.errorMessage = 'Identificador de proyecto inválido.';
      return;
    }
    this.projectId = projectId;
    this.loadProject(projectId);
  }

  loadProject(projectId: number): void {
    this.loading = true;
    this.errorMessage = null;
    this.projectService.getById(projectId).subscribe({
      next: (project) => {
        this.project = project;
        this.loading = false;
      },
      error: (err: HttpErrorResponse) => {
        this.loading = false;
        this.project = null;
        this.errorMessage = this.describeError(err);
      },
    });
  }

  onEditActivity(activity: ActivityWithIndicators): void {
    this.activityToEdit = activity;
    this.errorMessage = null;
  }

  onCancelActivityForm(): void {
    this.activityToEdit = null;
  }

  onSaveActivity(event: ActivityFormSaveEvent): void {
    if (this.projectId === null || this.savingActivity) {
      return;
    }

    this.savingActivity = true;
    this.errorMessage = null;

    const request$ =
      event.activityId === null
        ? this.projectService.createActivity(this.projectId, event.data)
        : this.activityService.update(event.activityId, event.data);

    request$.subscribe({
      next: () => {
        this.savingActivity = false;
        this.activityToEdit = null;
        this.activityForm?.close();
        this.loadProject(this.projectId!);
      },
      error: (err: HttpErrorResponse) => {
        this.savingActivity = false;
        this.errorMessage = this.describeMutationError(
          err,
          event.activityId === null
            ? 'No se pudo crear la actividad.'
            : 'No se pudo actualizar la actividad.',
        );
      },
    });
  }

  onRemoveActivity(activity: ActivityWithIndicators): void {
    const confirmed = window.confirm(
      `¿Eliminar la actividad "${activity.name}"?`,
    );
    if (!confirmed || this.projectId === null) {
      return;
    }

    this.activityService.delete(activity.id).subscribe({
      next: () => {
        if (this.activityToEdit?.id === activity.id) {
          this.activityToEdit = null;
          this.activityForm?.close();
        }
        this.loadProject(this.projectId!);
      },
      error: (err: HttpErrorResponse) => {
        this.errorMessage = this.describeMutationError(
          err,
          'No se pudo eliminar la actividad.',
        );
      },
    });
  }

  private describeError(err: HttpErrorResponse): string {
    if (err.status === 0) {
      return 'No hay conexión con la API. ¿Está corriendo en http://localhost:8000?';
    }
    if (err.status === 404) {
      return 'Proyecto no encontrado.';
    }
    if (typeof err.error?.detail === 'string') {
      return err.error.detail;
    }
    return 'No se pudo cargar el proyecto.';
  }

  private describeMutationError(err: HttpErrorResponse, fallback: string): string {
    if (err.status === 0) {
      return 'No hay conexión con la API. ¿Está corriendo en http://localhost:8000?';
    }
    if (typeof err.error?.detail === 'string') {
      return err.error.detail;
    }
    if (Array.isArray(err.error?.detail)) {
      return 'Revisa los datos del formulario (la API rechazó la validación).';
    }
    return fallback;
  }
}
