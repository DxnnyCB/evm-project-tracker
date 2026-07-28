import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { ProjectService } from '../../../core/services/project.service';
import { Project } from '../../../models/project.model';
import { ConfirmDialogComponent } from '../../../shared/components/confirm-dialog/confirm-dialog.component';
import { ToastService } from '../../../shared/services/toast.service';

@Component({
  selector: 'app-project-list',
  imports: [FormsModule, RouterLink, ConfirmDialogComponent],
  templateUrl: './project-list.component.html',
  styleUrl: './project-list.component.css',
})
export class ProjectListComponent implements OnInit {
  private readonly projectService = inject(ProjectService);
  private readonly toast = inject(ToastService);

  projects: Project[] = [];
  newProjectName = '';
  loading = false;
  creating = false;
  errorMessage: string | null = null;

  confirmOpen = false;
  confirmTitle = '';
  confirmMessage = '';
  private pendingDelete: Project | null = null;

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {
    this.loading = true;
    this.errorMessage = null;
    this.projectService.list().subscribe({
      next: (projects) => {
        this.projects = projects;
        this.loading = false;
      },
      error: (err: HttpErrorResponse) => {
        this.loading = false;
        this.errorMessage = this.describeError(
          err,
          'No se pudo cargar la lista de proyectos.',
        );
      },
    });
  }

  createProject(): void {
    const name = this.newProjectName.trim();
    if (!name || this.creating) {
      return;
    }

    this.creating = true;
    this.errorMessage = null;
    this.projectService.create({ name }).subscribe({
      next: (project) => {
        this.projects = [...this.projects, project];
        this.newProjectName = '';
        this.creating = false;
        this.toast.success(`Proyecto "${project.name}" creado.`);
      },
      error: (err: HttpErrorResponse) => {
        this.creating = false;
        const message = this.describeError(err, 'No se pudo crear el proyecto.');
        this.errorMessage = message;
        this.toast.error(message);
      },
    });
  }

  deleteProject(project: Project, event: Event): void {
    event.stopPropagation();
    event.preventDefault();
    this.pendingDelete = project;
    this.confirmTitle = 'Eliminar proyecto';
    this.confirmMessage =
      `¿Eliminar el proyecto "${project.name}"?\nSe borrarán también todas sus actividades.`;
    this.confirmOpen = true;
  }

  onConfirmDelete(): void {
    const project = this.pendingDelete;
    this.closeConfirm();
    if (!project) {
      return;
    }

    this.errorMessage = null;
    this.projectService.delete(project.id).subscribe({
      next: () => {
        this.projects = this.projects.filter((p) => p.id !== project.id);
        this.toast.success(`Proyecto "${project.name}" eliminado.`);
      },
      error: (err: HttpErrorResponse) => {
        const message = this.describeError(
          err,
          'No se pudo eliminar el proyecto.',
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

  private describeError(err: HttpErrorResponse, fallback: string): string {
    if (err.status === 0) {
      return 'No hay conexión con la API. ¿Está corriendo en http://localhost:8000?';
    }
    if (typeof err.error?.detail === 'string') {
      return err.error.detail;
    }
    return fallback;
  }
}
