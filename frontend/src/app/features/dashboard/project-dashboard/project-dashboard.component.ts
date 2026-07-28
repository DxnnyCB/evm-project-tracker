import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, ViewChild, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ActivityService } from '../../../core/services/activity.service';
import { ProjectService } from '../../../core/services/project.service';
import {
  ActivityFormComponent,
  ActivityFormSaveEvent,
} from '../../activities/activity-form/activity-form.component';
import { ActivityTableComponent } from '../../activities/activity-table/activity-table.component';
import { ConsolidatedPanelComponent } from '../../activities/consolidated-panel/consolidated-panel.component';
import { EvmChartComponent } from '../../activities/evm-chart/evm-chart.component';
import { ActivityWithIndicators } from '../../../models/activity.model';
import { ProjectDetail } from '../../../models/project.model';
import { ConfirmDialogComponent } from '../../../shared/components/confirm-dialog/confirm-dialog.component';
import { ToastService } from '../../../shared/services/toast.service';

@Component({
  selector: 'app-project-dashboard',
  imports: [
    FormsModule,
    RouterLink,
    ConsolidatedPanelComponent,
    ActivityTableComponent,
    ActivityFormComponent,
    EvmChartComponent,
    ConfirmDialogComponent,
  ],
  templateUrl: './project-dashboard.component.html',
  styleUrl: './project-dashboard.component.css',
})
export class ProjectDashboardComponent implements OnInit {
  @ViewChild(ActivityFormComponent) private activityForm?: ActivityFormComponent;

  private readonly route = inject(ActivatedRoute);
  private readonly projectService = inject(ProjectService);
  private readonly activityService = inject(ActivityService);
  private readonly toast = inject(ToastService);

  project: ProjectDetail | null = null;
  activityToEdit: ActivityWithIndicators | null = null;
  loading = false;
  savingActivity = false;
  savingProjectName = false;
  editingProjectName = false;
  projectNameDraft = '';
  errorMessage: string | null = null;
  private projectId: number | null = null;

  confirmOpen = false;
  confirmTitle = '';
  confirmMessage = '';
  private pendingDelete: ActivityWithIndicators | null = null;

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

  startEditProjectName(): void {
    if (!this.project || this.savingProjectName) {
      return;
    }
    this.projectNameDraft = this.project.name;
    this.editingProjectName = true;
  }

  cancelEditProjectName(): void {
    this.editingProjectName = false;
    this.projectNameDraft = '';
  }

  saveProjectName(): void {
    if (this.projectId === null || !this.project || this.savingProjectName) {
      return;
    }

    const name = this.projectNameDraft.trim();
    if (!name) {
      this.toast.error('El nombre del proyecto no puede estar vacío.');
      return;
    }
    if (name === this.project.name) {
      this.cancelEditProjectName();
      return;
    }

    this.savingProjectName = true;
    this.projectService.update(this.projectId, { name }).subscribe({
      next: (updated) => {
        this.project = { ...this.project!, name: updated.name };
        this.savingProjectName = false;
        this.editingProjectName = false;
        this.projectNameDraft = '';
        this.toast.success('Nombre del proyecto actualizado.');
      },
      error: (err: HttpErrorResponse) => {
        this.savingProjectName = false;
        const message = this.describeMutationError(
          err,
          'No se pudo actualizar el nombre del proyecto.',
        );
        this.errorMessage = message;
        this.toast.error(message);
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
    const isCreate = event.activityId === null;

    const request$ =
      isCreate
        ? this.projectService.createActivity(this.projectId, event.data)
        : this.activityService.update(event.activityId!, event.data);

    request$.subscribe({
      next: () => {
        this.savingActivity = false;
        this.activityToEdit = null;
        this.activityForm?.close();
        this.loadProject(this.projectId!);
        this.toast.success(
          isCreate ? 'Actividad creada.' : 'Actividad actualizada.',
        );
      },
      error: (err: HttpErrorResponse) => {
        this.savingActivity = false;
        const message = this.describeMutationError(
          err,
          isCreate
            ? 'No se pudo crear la actividad.'
            : 'No se pudo actualizar la actividad.',
        );
        this.errorMessage = message;
        this.toast.error(message);
      },
    });
  }

  onRemoveActivity(activity: ActivityWithIndicators): void {
    this.pendingDelete = activity;
    this.confirmTitle = 'Eliminar actividad';
    this.confirmMessage = `¿Eliminar la actividad "${activity.name}"?`;
    this.confirmOpen = true;
  }

  onConfirmDelete(): void {
    const activity = this.pendingDelete;
    this.closeConfirm();
    if (!activity || this.projectId === null) {
      return;
    }

    this.activityService.delete(activity.id).subscribe({
      next: () => {
        if (this.activityToEdit?.id === activity.id) {
          this.activityToEdit = null;
          this.activityForm?.close();
        }
        this.loadProject(this.projectId!);
        this.toast.success(`Actividad "${activity.name}" eliminada.`);
      },
      error: (err: HttpErrorResponse) => {
        const message = this.describeMutationError(
          err,
          'No se pudo eliminar la actividad.',
        );
        this.errorMessage = message;
        this.toast.error(message);
      },
    });
  }

  onCancelDelete(): void {
    this.closeConfirm();
  }

  private closeConfirm(): void {
    this.confirmOpen = false;
    this.pendingDelete = null;
    this.confirmTitle = '';
    this.confirmMessage = '';
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
