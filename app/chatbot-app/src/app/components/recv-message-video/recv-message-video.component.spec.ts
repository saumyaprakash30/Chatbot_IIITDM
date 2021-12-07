import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecvMessageVideoComponent } from './recv-message-video.component';

describe('RecvMessageVideoComponent', () => {
  let component: RecvMessageVideoComponent;
  let fixture: ComponentFixture<RecvMessageVideoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecvMessageVideoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RecvMessageVideoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
