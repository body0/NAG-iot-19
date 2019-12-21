import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule, MatInputModule, MatToolbarModule, MatIconModule, MatSidenavModule,
   MatListModule, MatCheckboxModule, MatExpansionModule, MatDialogModule, MatDividerModule,
    MatRippleModule, MatSnackBarModule, MatTabsModule, MatSelectModule, MatSliderModule } from '@angular/material';
import { FormsModule } from '@angular/forms';

const MaterialDependenci = [
  MatButtonModule,
  MatInputModule,
  MatToolbarModule,
  MatSidenavModule,
  MatIconModule,
  MatListModule,
  MatCheckboxModule,
  MatExpansionModule,
  MatDialogModule,
  MatDividerModule,
  MatRippleModule,
  MatSnackBarModule,
  MatTabsModule,
  MatSelectModule,
  MatSliderModule
];

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MaterialDependenci
  ],
  exports: [
    MaterialDependenci
  ]
})
export class MaterialModule { }
