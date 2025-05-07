import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavComponent } from './nav/nav.component';
import { SidenavComponent } from './sidenav/sidenav.component';
import { FooterComponent } from './footer/footer.component';
import { RouterModule } from '@angular/router';
import {
  LucideAngularModule,
  BarChart2,
  Brain,
  FileText,
  HelpCircle,
  Home,
  Settings,
  Upload,
  Users,
} from 'lucide-angular';
import { HeaderComponent } from './header/header.component';

@NgModule({
  declarations: [
    NavComponent,
    SidenavComponent,
    FooterComponent,
    HeaderComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    LucideAngularModule.pick({
      Home,
      Brain,
      Upload,
      BarChart2,
      FileText,
      Users,
      Settings,
      HelpCircle,
    }),
  ],
  exports: [NavComponent, SidenavComponent, FooterComponent, HeaderComponent],
})
export class LayoutsModule {}
