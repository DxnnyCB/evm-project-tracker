import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ProjectService } from '../../../core/services/project.service';
import { ConsolidatedPanelComponent } from '../../activities/consolidated-panel/consolidated-panel.component';
import { ProjectDetail } from '../../../models/project.model';

@Component({
  selector: 'app-project-dashboard',
  imports: [RouterLink, ConsolidatedPanelComponent],
  templateUrl: './project-dashboard.component.html',
  styleUrl: './project-dashboard.component.css',
})
export class ProjectDashboardComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly projectService = inject(ProjectService);

  project: ProjectDetail | null = null;
  loading = false;
  errorMessage: string | null = null;

  ngOnInit(): void {
    const rawId = this.route.snapshot.paramMap.get('projectId');
    const projectId = rawId ? Number(rawId) : NaN;
    if (!Number.isInteger(projectId) || projectId <= 0) {
      this.errorMessage = 'Identificador de proyecto inválido.';
      return;
    }
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
}
