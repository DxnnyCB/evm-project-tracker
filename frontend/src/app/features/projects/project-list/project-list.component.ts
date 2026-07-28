import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { ProjectService } from '../../../core/services/project.service';
import { Project } from '../../../models/project.model';

@Component({
  selector: 'app-project-list',
  imports: [FormsModule, RouterLink],
  templateUrl: './project-list.component.html',
  styleUrl: './project-list.component.css',
})
export class ProjectListComponent implements OnInit {
  private readonly projectService = inject(ProjectService);

  projects: Project[] = [];
  newProjectName = '';
  loading = false;
  creating = false;
  errorMessage: string | null = null;

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
      },
      error: (err: HttpErrorResponse) => {
        this.creating = false;
        this.errorMessage = this.describeError(
          err,
          'No se pudo crear el proyecto.',
        );
      },
    });
  }

  deleteProject(project: Project, event: Event): void {
    event.stopPropagation();
    event.preventDefault();

    const confirmed = window.confirm(
      `¿Eliminar el proyecto "${project.name}"?\nSe borrarán también todas sus actividades.`,
    );
    if (!confirmed) {
      return;
    }

    this.errorMessage = null;
    this.projectService.delete(project.id).subscribe({
      next: () => {
        this.projects = this.projects.filter((p) => p.id !== project.id);
      },
      error: (err: HttpErrorResponse) => {
        this.errorMessage = this.describeError(
          err,
          'No se pudo eliminar el proyecto.',
        );
      },
    });
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
