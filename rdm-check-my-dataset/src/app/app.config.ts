import {
  APP_INITIALIZER,
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
} from '@angular/core';
import { provideRouter, withInMemoryScrolling } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { providePrimeNG } from 'primeng/config';
import { definePreset } from '@primeuix/themes';
import Lara from '@primeuix/themes/lara';
import { routes } from './app.routes';
import { Config } from './services/config';
export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes, withInMemoryScrolling({ anchorScrolling: 'enabled' })),
    provideHttpClient(),
    providePrimeNG({
      theme: {
        preset: definePreset(Lara, {
          semantic: {
            primary: {
              50: '{blue.50}',
              100: '{blue.100}',
              200: '{blue.200}',
              300: '{blue.300}',
              400: '{blue.400}',
              500: '{blue.500}',
              600: '{blue.600}',
              700: '{blue.700}',
              800: '{blue.800}',
              900: '{blue.900}',
              950: '{blue.950}',
            },
          },
        }),
      },
    }),
    {
      provide: APP_INITIALIZER,
      multi: true,
      deps: [Config],
      useFactory: (appConfigService: Config) => {
        return () => {
          return appConfigService.loadConfig();
        };
      },
    },
    
  ],
};
